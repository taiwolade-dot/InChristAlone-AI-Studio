from datetime import datetime, date
from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models import (
    db,
    Member,
    ChurchProfile,
    ChurchBrandProfile,
    ActivityLog,
    MinistryContent
)
from modules.ai_assistant.member_intelligence import (
    get_member_ai_summary,
    calculate_member_care_score,
    generate_member_care_recommendations
)

church_management_bp = Blueprint(
    'church_management',
    __name__,
    url_prefix='/church-management',
    template_folder='templates',
    static_folder='static',
    static_url_path='/church-management/static'
)



UPLOAD_FOLDER = 'modules/church_management/static/uploads'

ALLOWED_EXTENSIONS = {
    'png',
    'jpg',
    'jpeg',
    'webp'
}


def allowed_file(filename):
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )




def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Church Management is only available to church admin/pastor accounts. Contact your studio administrator to request admin access.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@church_management_bp.route('/profile', methods=['GET'])
@login_required
@admin_required
def church_profile():

    profile = ChurchProfile.query.filter_by(
        owner_id=current_user.id
    ).first()

    if not profile:
        return redirect(
            url_for('church_management.create_church_profile')
        )

    return render_template(
        'church_management/profile.html',
        profile=profile
    )



@church_management_bp.route('/brand', methods=['GET', 'POST'])
@login_required
@admin_required
def church_brand():

    profile = ChurchProfile.query.filter_by(
        owner_id=current_user.id
    ).first()

    if not profile:
        return redirect(
            url_for('church_management.create_church_profile')
        )

    brand = ChurchBrandProfile.query.filter_by(
        church_id=profile.id
    ).first()

    if request.method == 'POST':

        if not brand:
            brand = ChurchBrandProfile(
                church_id=profile.id
            )

        brand.primary_color = request.form.get('primary_color')
        brand.accent_color = request.form.get('accent_color')
        brand.visual_style = request.form.get('visual_style')
        brand.ministry_tone = request.form.get('ministry_tone')
        brand.preferred_layout = request.form.get('preferred_layout')
        brand.logo_position = request.form.get('logo_position')

        db.session.add(brand)
        db.session.commit()

        flash(
            'Church AI Brand Identity updated successfully.',
            'success'
        )

        return redirect(
            url_for('church_management.church_brand')
        )

    return render_template(
        'church_management/brand.html',
        profile=profile,
        brand=brand
    )


@church_management_bp.route('/profile/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_church_profile():

    if request.method == 'POST':

        logo_filename = None

        logo = request.files.get('logo')

        if logo and allowed_file(logo.filename):
            filename = secure_filename(logo.filename)
            logo.save(
                f'{UPLOAD_FOLDER}/{filename}'
            )
            logo_filename = filename


        founded_date = (
            datetime.strptime(request.form.get("founded_date"), "%Y-%m-%d").date()
            if request.form.get("founded_date") else None
        )

        organized_date = (
            datetime.strptime(request.form.get("organized_date"), "%Y-%m-%d").date()
            if request.form.get("organized_date") else None
        )

        profile = ChurchProfile(
            owner_id=current_user.id,
            church_name=request.form.get('church_name'),
            motto=request.form.get('motto'),
            vision=request.form.get('vision'),
            mission=request.form.get('mission'),
            denomination=request.form.get('denomination'),
            association=request.form.get('association'),
            conference=request.form.get('conference'),
            address=request.form.get('address'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            website=request.form.get('website'),
            logo_filename=logo_filename,
            founded_date=founded_date,
            organized_date=organized_date,
            statement_of_faith=request.form.get('statement_of_faith')
        )

        db.session.add(profile)
        db.session.commit()

        flash(
            'Church Profile created successfully.',
            'success'
        )

        return redirect(
            url_for('church_management.church_profile')
        )

    return render_template(
        'church_management/profile_form.html'
    )


@church_management_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_church_profile():

    profile = ChurchProfile.query.filter_by(
        owner_id=current_user.id
    ).first()

    if not profile:
        return redirect(
            url_for('church_management.create_church_profile')
        )

    if request.method == 'POST':

        logo = request.files.get('logo')

        if logo and allowed_file(logo.filename):
            filename = secure_filename(logo.filename)
            logo.save(
                f'{UPLOAD_FOLDER}/{filename}'
            )
            profile.logo_filename = filename


        edit_founded_date = (
            datetime.strptime(request.form.get("founded_date"), "%Y-%m-%d").date()
            if request.form.get("founded_date") else None
        )

        edit_organized_date = (
            datetime.strptime(request.form.get("organized_date"), "%Y-%m-%d").date()
            if request.form.get("organized_date") else None
        )

        profile.church_name = request.form.get('church_name')
        profile.motto = request.form.get('motto')
        profile.vision = request.form.get('vision')
        profile.mission = request.form.get('mission')
        profile.denomination = request.form.get('denomination')
        profile.association = request.form.get('association')
        profile.conference = request.form.get('conference')
        profile.address = request.form.get('address')
        profile.phone = request.form.get('phone')
        profile.email = request.form.get('email')
        profile.website = request.form.get('website')
        profile.founded_date = edit_founded_date
        profile.organized_date = edit_organized_date
        profile.statement_of_faith = request.form.get('statement_of_faith')

        db.session.commit()

        flash(
            'Church Profile updated successfully.',
            'success'
        )

        return redirect(
            url_for('church_management.church_profile')
        )

    return render_template(
        'church_management/profile_form.html',
        profile=profile
    )


@church_management_bp.route('/', methods=['GET'])
@login_required
@admin_required
def index():
    from datetime import date
    from sqlalchemy import extract

    filter_month = request.args.get('birthday_month', '')

    query = Member.query.filter_by(owner_id=current_user.id)

    if filter_month:
        query = query.filter(extract('month', Member.birthday) == int(filter_month))
        query = query.order_by(extract('day', Member.birthday))
    else:
        query = query.order_by(Member.full_name)

    members = query.all()

    today = date.today()
    today_birthdays = Member.query.filter_by(owner_id=current_user.id).filter(
        extract('month', Member.birthday) == today.month,
        extract('day', Member.birthday) == today.day
    ).all()

    return render_template(
        'church_management/index.html',
        members=members,
        filter_month=filter_month,
        today_birthdays=today_birthdays
    )


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
        date_of_salvation_str = request.form.get('date_of_salvation', '').strip()
        date_of_baptism_str = request.form.get('date_of_baptism', '').strip()
        marital_status = request.form.get('marital_status', '').strip()
        age_range = request.form.get('age_range', '').strip()

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

        date_of_salvation = None
        if date_of_salvation_str:
            try:
                date_of_salvation = datetime.strptime(date_of_salvation_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        date_of_baptism = None
        if date_of_baptism_str:
            try:
                date_of_baptism = datetime.strptime(date_of_baptism_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        new_member = Member(
            owner_id=current_user.id,
            full_name=full_name,
            phone=phone,
            email=email,
            address=address,
            church_role=church_role,
            date_joined=date_joined,
            date_of_salvation=date_of_salvation,
            date_of_baptism=date_of_baptism,
            marital_status=marital_status,
            age_range=age_range,
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
    if member.owner_id != current_user.id:
        flash('You do not have permission to edit this member.', 'error')
        return redirect(url_for('church_management.index'))

    if request.method == 'POST':
        member.full_name = request.form.get('full_name', '').strip()
        member.phone = request.form.get('phone', '').strip()
        member.email = request.form.get('email', '').strip()
        member.address = request.form.get('address', '').strip()
        member.church_role = request.form.get('church_role', '').strip()
        member.marital_status = request.form.get('marital_status', '').strip()
        member.age_range = request.form.get('age_range', '').strip()
        member.notes = request.form.get('notes', '').strip()

        date_joined_str = request.form.get('date_joined', '').strip()
        if date_joined_str:
            try:
                member.date_joined = datetime.strptime(date_joined_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format for date joined. Please use YYYY-MM-DD.', 'error')
                return render_template('church_management/edit_member.html', member=member)
        else:
            member.date_joined = None

        birthday_str = request.form.get('birthday', '').strip()
        if birthday_str:
            try:
                member.birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format for birthday. Please use YYYY-MM-DD.', 'error')
                return render_template('church_management/edit_member.html', member=member)
        else:
            member.birthday = None

        date_of_salvation_str = request.form.get('date_of_salvation', '').strip()
        if date_of_salvation_str:
            try:
                member.date_of_salvation = datetime.strptime(date_of_salvation_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        else:
            member.date_of_salvation = None

        date_of_baptism_str = request.form.get('date_of_baptism', '').strip()
        if date_of_baptism_str:
            try:
                member.date_of_baptism = datetime.strptime(date_of_baptism_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        else:
            member.date_of_baptism = None
            member.birthday = None

        try:
            db.session.commit()
            flash('Member updated successfully!', 'success')
            return redirect(url_for('church_management.index'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the member.', 'error')

    return render_template('church_management/edit_member.html', member=member)



@church_management_bp.route('/members/<int:member_id>')
@login_required
@admin_required
def member_profile(member_id):

    member = Member.query.get_or_404(member_id)

    if member.owner_id != current_user.id:
        flash(
            'You do not have permission to view this member.',
            'error'
        )
        return redirect(
            url_for('church_management.index')
        )

    member_ai_summary = get_member_ai_summary(
        member.full_name
    )

    member_care_score = calculate_member_care_score(
        member.full_name
    )

    member_recommendations = generate_member_care_recommendations(
        member.full_name
    )

    return render_template(
        'church_management/member_profile.html',
        member=member,
        member_ai_summary=member_ai_summary,
        member_care_score=member_care_score,
        member_recommendations=member_recommendations,
        ai_activities=member_ai_summary["history"],
        ai_content=member_ai_summary["history"]
    )


@church_management_bp.route('/delete/<int:member_id>', methods=['POST'])
@login_required
@admin_required
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    if member.owner_id != current_user.id:
        flash('You do not have permission to delete this member.', 'error')
        return redirect(url_for('church_management.index'))
    name = member.full_name
    db.session.delete(member)
    db.session.commit()
    flash(f'{name} removed.', 'info')
    return redirect(url_for('church_management.index'))
