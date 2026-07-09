from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models import db, User, PromptPack, Purchase, WalletTransaction

admin_panel_bp = Blueprint(
    'admin_panel',
    __name__,
    url_prefix='/admin-panel',
    template_folder='../../templates/admin_panel'
)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You do not have permission to access the Admin Panel.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@admin_panel_bp.route('/', methods=['GET'])
@login_required
@admin_required
def index():
    active_tab = request.args.get('tab', 'stats')

    total_users = User.query.count()
    total_packs = PromptPack.query.count()
    total_purchases = Purchase.query.count()
    successful_recharges = WalletTransaction.query.filter_by(status='success').all()
    total_revenue_naira = sum(t.amount_naira for t in successful_recharges)

    users = User.query.order_by(User.created_at.desc()).all()
    packs = PromptPack.query.order_by(PromptPack.created_at.desc()).all()

    return render_template(
        'admin_panel/index.html',
        active_tab=active_tab,
        total_users=total_users,
        total_packs=total_packs,
        total_purchases=total_purchases,
        total_revenue_naira=total_revenue_naira,
        users=users,
        packs=packs
    )


@admin_panel_bp.route('/user/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash('You cannot change your own admin status.', 'error')
        return redirect(url_for('admin_panel.index', tab='users'))

    user.role = 'member' if user.role == 'admin' else 'admin'
    db.session.commit()
    flash(f'{user.full_name} is now {user.role}.', 'success')
    return redirect(url_for('admin_panel.index', tab='users'))


@admin_panel_bp.route('/user/<int:user_id>/adjust-wallet', methods=['POST'])
@login_required
@admin_required
def adjust_wallet(user_id):
    user = User.query.get_or_404(user_id)

    try:
        adjustment = int(request.form.get('adjustment', 0))
    except ValueError:
        adjustment = 0

    user.wallet_balance = max(0, user.wallet_balance + adjustment)
    db.session.commit()
    flash(f"{user.full_name}'s wallet adjusted to {user.wallet_balance} units.", 'success')
    return redirect(url_for('admin_panel.index', tab='users'))


@admin_panel_bp.route('/pack/<int:pack_id>/toggle-active', methods=['POST'])
@login_required
@admin_required
def toggle_pack_active(pack_id):
    pack = PromptPack.query.get_or_404(pack_id)
    pack.is_active = not pack.is_active
    db.session.commit()
    status = 'activated' if pack.is_active else 'deactivated'
    flash(f'"{pack.title}" {status}.', 'success')
    return redirect(url_for('admin_panel.index', tab='packs'))


@admin_panel_bp.route('/pack/<int:pack_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_pack(pack_id):
    pack = PromptPack.query.get_or_404(pack_id)

    if request.method == 'POST':
        pack.title = request.form.get('title', '').strip()
        pack.description = request.form.get('description', '').strip()
        pack.category = request.form.get('category', '').strip()
        pack.content = request.form.get('content', '').strip()

        try:
            pack.price_units = int(request.form.get('price_units', pack.price_units))
        except ValueError:
            pass

        db.session.commit()
        flash(f'"{pack.title}" updated.', 'success')
        return redirect(url_for('admin_panel.index', tab='packs'))

    return render_template('admin_panel/edit_pack.html', pack=pack)