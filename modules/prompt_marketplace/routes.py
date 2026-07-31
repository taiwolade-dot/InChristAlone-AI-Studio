import os
import uuid
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models import db, PromptPack, Purchase, WalletTransaction
from .paystack_service import initialize_transaction, verify_transaction

prompt_marketplace_bp = Blueprint(
    'prompt_marketplace',
    __name__,
    url_prefix='/marketplace',
    template_folder='../../templates/prompt_marketplace'
)

UNITS_PER_NAIRA = 0.1
MIN_RECHARGE_NAIRA = 500
RECHARGE_ENABLED = False  # Set to True once Paystack live account is verified
UPLOAD_FOLDER = os.path.join('uploads', 'prompt_packs')
ALLOWED_EXTENSIONS = {'pdf'}


def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _ensure_upload_folder():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@prompt_marketplace_bp.route('/', methods=['GET'])
@login_required
def index():
    packs = PromptPack.query.filter_by(is_active=True).order_by(PromptPack.created_at.desc()).all()
    purchased_pack_ids = {p.pack_id for p in current_user.purchases}
    return render_template(
        'prompt_marketplace/index.html',
        packs=packs,
        purchased_pack_ids=purchased_pack_ids
    )


@prompt_marketplace_bp.route('/pack/<int:pack_id>', methods=['GET'])
@login_required
def pack_detail(pack_id):
    pack = PromptPack.query.get_or_404(pack_id)
    already_purchased = Purchase.query.filter_by(user_id=current_user.id, pack_id=pack.id).first() is not None
    return render_template(
        'prompt_marketplace/pack_detail.html',
        pack=pack,
        already_purchased=already_purchased
    )


@prompt_marketplace_bp.route('/pack/<int:pack_id>/purchase', methods=['POST'])
@login_required
def purchase_pack(pack_id):
    pack = PromptPack.query.get_or_404(pack_id)

    already_purchased = Purchase.query.filter_by(user_id=current_user.id, pack_id=pack.id).first()
    if already_purchased:
        flash('You already own this prompt pack.', 'info')
        return redirect(url_for('prompt_marketplace.pack_detail', pack_id=pack.id))

    if current_user.wallet_balance < pack.price_units:
        flash(f'Insufficient units. You need {pack.price_units} units but have {current_user.wallet_balance}.', 'error')
        return redirect(url_for('prompt_marketplace.recharge'))

    current_user.wallet_balance -= pack.price_units
    new_purchase = Purchase(
        user_id=current_user.id,
        pack_id=pack.id,
        units_spent=pack.price_units
    )
    db.session.add(new_purchase)
    db.session.commit()

    flash(f'"{pack.title}" unlocked successfully!', 'success')
    return redirect(url_for('prompt_marketplace.pack_detail', pack_id=pack.id))


@prompt_marketplace_bp.route('/pack/<int:pack_id>/download', methods=['GET'])
@login_required
def download_pdf(pack_id):
    pack = PromptPack.query.get_or_404(pack_id)

    if not pack.pdf_filename:
        flash('No PDF available for this pack.', 'error')
        return redirect(url_for('prompt_marketplace.pack_detail', pack_id=pack.id))

    already_purchased = Purchase.query.filter_by(user_id=current_user.id, pack_id=pack.id).first()
    if not already_purchased:
        flash('You must unlock this pack before downloading.', 'error')
        return redirect(url_for('prompt_marketplace.pack_detail', pack_id=pack.id))

    return send_from_directory(
        os.path.abspath(UPLOAD_FOLDER),
        pack.pdf_filename,
        as_attachment=True,
        download_name=pack.pdf_filename.split('_', 1)[-1]
    )


@prompt_marketplace_bp.route('/recharge', methods=['GET'])
@login_required
def recharge():
    return render_template(
        'prompt_marketplace/recharge.html',
        min_recharge=MIN_RECHARGE_NAIRA,
        wallet_balance=current_user.wallet_balance
    )


@prompt_marketplace_bp.route('/recharge/initiate', methods=['POST'])
@login_required
def initiate_recharge():
    if not RECHARGE_ENABLED:
        flash("Wallet recharge is temporarily unavailable. Please contact your studio administrator for Units.", "error")
        return redirect(url_for("prompt_marketplace.recharge"))
    try:
        amount_naira = int(request.form.get('amount_naira', 0))
    except ValueError:
        amount_naira = 0

    if amount_naira < MIN_RECHARGE_NAIRA:
        flash(f'Minimum recharge is ₦{MIN_RECHARGE_NAIRA}.', 'error')
        return redirect(url_for('prompt_marketplace.recharge'))

    reference = f"ICA-{uuid.uuid4().hex[:12]}"
    units_to_add = int(amount_naira * UNITS_PER_NAIRA)

    wallet_txn = WalletTransaction(
        user_id=current_user.id,
        reference=reference,
        amount_naira=amount_naira,
        units_added=units_to_add,
        status='pending'
    )
    db.session.add(wallet_txn)
    db.session.commit()

    callback_url = url_for('prompt_marketplace.verify_recharge', _external=True)

    result = initialize_transaction(
        email=current_user.email,
        amount_naira=amount_naira,
        callback_url=callback_url,
        reference=reference
    )

    if result['success']:
        return redirect(result['authorization_url'])
    else:
        flash(f"Payment initialization failed: {result['message']}", 'error')
        return redirect(url_for('prompt_marketplace.recharge'))


@prompt_marketplace_bp.route('/recharge/verify', methods=['GET'])
@login_required
def verify_recharge():
    reference = request.args.get('reference') or request.args.get('trxref')

    if not reference:
        flash('No transaction reference found.', 'error')
        return redirect(url_for('prompt_marketplace.recharge'))

    wallet_txn = WalletTransaction.query.filter_by(reference=reference).first()

    if not wallet_txn:
        flash('Transaction not found.', 'error')
        return redirect(url_for('prompt_marketplace.recharge'))

    if wallet_txn.status == 'success':
        flash('This transaction was already processed.', 'info')
        return redirect(url_for('prompt_marketplace.index'))

    result = verify_transaction(reference)

    if result['success'] and result['status'] == 'success':
        wallet_txn.status = 'success'
        current_user.wallet_balance += wallet_txn.units_added
        db.session.commit()
        flash(f'Recharge successful! {wallet_txn.units_added} units added to your wallet.', 'success')
        return redirect(url_for('prompt_marketplace.index'))
    else:
        wallet_txn.status = 'failed'
        db.session.commit()
        flash('Payment verification failed. Please try again.', 'error')
        return redirect(url_for('prompt_marketplace.recharge'))


@prompt_marketplace_bp.route('/admin/add-pack', methods=['GET', 'POST'])
@login_required
def add_pack():
    if not current_user.is_admin():
        flash('You do not have permission to add prompt packs.', 'error')
        return redirect(url_for('prompt_marketplace.index'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        content = request.form.get('content', '').strip()

        try:
            price_units = int(request.form.get('price_units', 0))
        except ValueError:
            price_units = 0

        if not title or price_units <= 0:
            flash('Title and a valid price are required.', 'error')
            return redirect(url_for('prompt_marketplace.add_pack'))

        pdf_filename = None
        if 'pdf_file' in request.files:
            pdf_file = request.files['pdf_file']
            if pdf_file.filename != '':
                if not _allowed_file(pdf_file.filename):
                    flash('Only PDF files are allowed.', 'error')
                    return redirect(url_for('prompt_marketplace.add_pack'))
                _ensure_upload_folder()
                safe_name = secure_filename(pdf_file.filename)
                pdf_filename = f"{uuid.uuid4().hex}_{safe_name}"
                pdf_file.save(os.path.join(UPLOAD_FOLDER, pdf_filename))

        if not content and not pdf_filename:
            flash('Please provide either text content or a PDF file.', 'error')
            return redirect(url_for('prompt_marketplace.add_pack'))

        new_pack = PromptPack(
            title=title,
            description=description,
            category=category,
            price_units=price_units,
            content=content,
            pdf_filename=pdf_filename
        )
        db.session.add(new_pack)
        db.session.commit()

        flash(f'"{title}" added to the marketplace.', 'success')
        return redirect(url_for('prompt_marketplace.index'))

    return render_template('prompt_marketplace/add_pack.html')