from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models import db, ContactMessage

support_bp = Blueprint(
    'support',
    __name__,
    template_folder='../../templates/support'
)


@support_bp.route('/about', methods=['GET'])
def about():
    return render_template('support/about.html')


@support_bp.route('/contact', methods=['GET'])
@login_required
def contact():
    my_messages = ContactMessage.query.filter_by(user_id=current_user.id).order_by(ContactMessage.created_at.desc()).all()
    return render_template('support/contact.html', my_messages=my_messages)


@support_bp.route('/contact/submit', methods=['POST'])
@login_required
def contact_submit():
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()

    if not subject or not message:
        flash('Please fill in both subject and message.', 'error')
        return redirect(url_for('support.contact'))

    new_message = ContactMessage(
        user_id=current_user.id,
        subject=subject,
        message=message
    )
    db.session.add(new_message)
    db.session.commit()

    flash('Your message has been sent. An admin will respond soon.', 'success')
    return redirect(url_for('support.contact'))
