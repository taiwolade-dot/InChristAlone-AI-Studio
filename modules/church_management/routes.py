from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models import db, Member

church_management_bp = Blueprint(
    'church_management',
    __name__,
    url_prefix='/church-management',
    template_folder='../../templates/church_management'
)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Church Management is only available to church admin/pastor accounts. Contact your studio administrator to request admin access.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@church_management_bp.route('/', methods=['GET'])
@login_required
@admin_required
def index():
    members = Member.query.order_by(Member.full_name).all()
    return render_template('church_management/index.html', members=members)


@church_management_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_member():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        church_role = request.form.get('church_role', '').strip()
        date_joined_str = request.form.get('date_joined', '').strip()
        birthday_str = request.form.get('birthday', '').strip()
        notes = request.form.get('notes', '').strip()

        if not full_name:
            flash('Full name is required.', 'error')
            return redirect(url_for('church_management.add_member'))

        date_joined = None
        if date_joined_str:
            try:
                date_joined = datetime.strptime(date_joined_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        birthday = None
        if birthday_str:
            try:
                birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        new_member = Member(
            full_name=full_name,
            phone=phone,
            email=email,
            address=address,
            church_role=church_role,
            date_joined=date_joined,
            birthday=birthday,
            notes=notes
        )
        db.session.add(new_member)
        db.session.commit()

        flash(f'{full_name} added successfully.', 'success')
        return redirect(url_for('church_management.index'))

    return render_template('church_management/add_member.html')


@church_management_bp.route('/edit/<int:member_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_member(member_id):
    member = Member.query.get_or_404(member_id)

    if request.method == 'POST':
        member.full_name = request.form.get('full_name', '').strip()
        member.phone = request.form.get('phone', '').strip()
        member.email = request.form.get('email', '').strip()
        member.address = request.form.get('address', '').strip()
        member.church_role = request.form.get('church_role', '').strip()
        member.notes = request.form.get('notes', '').strip()

        date_joined_str = request.form.get('date_joined', '').strip()
        if date_joined_str:
            try:
                member.date_joined = datetime.strptime(date_joined_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        birthday_str = request.form.get('birthday', '').strip()
        if birthday_str:
            try:
                member.birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        db.session.commit()
        flash(f'{member.full_name} updated successfully.', 'success')
        return redirect(url_for('church_management.index'))

    return render_template('church_management/edit_member.html', member=member)


@church_management_bp.route('/delete/<int:member_id>', methods=['POST'])
@login_required
@admin_required
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    name = member.full_name
    db.session.delete(member)
    db.session.commit()
    flash(f'{name} removed.', 'info')
    return redirect(url_for('church_management.index'))