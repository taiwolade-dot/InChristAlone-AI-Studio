from datetime import datetime, date
from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models import db, ChurchProfile, PastorProfile


pastor_management_bp = Blueprint(
    'pastor_management',
    __name__,
    url_prefix='/pastor-management',
    template_folder='templates',
    static_folder='static',
    static_url_path='/pastor-management/static'
)


UPLOAD_FOLDER = 'modules/pastor_management/static/uploads'


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
            flash(
                'Pastor Management is only available to church admin/pastor accounts.',
                'error'
            )
            return redirect(url_for('dashboard'))

        return f(*args, **kwargs)

    return decorated_function


@pastor_management_bp.route('/profile/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_pastor_profile():

    church = ChurchProfile.query.filter_by(
        owner_id=current_user.id
    ).first()

    if not church:
        flash(
            'Please create your Church Profile first.',
            'error'
        )
        return redirect(
            url_for('church_management.create_church_profile')
        )


    if request.method == 'POST':

        photo_filename = None

        photo = request.files.get('photo')

        if photo and allowed_file(photo.filename):

            photo_filename = secure_filename(
                photo.filename
            )

            photo.save(
                f"{UPLOAD_FOLDER}/{photo_filename}"
            )


        called_date = request.form.get(
            'called_to_church_date'
        )

        if called_date:
            called_date = datetime.strptime(
                called_date,
                '%Y-%m-%d'
            ).date()


        pastor = PastorProfile(
            church_id=church.id,
            full_name=request.form.get('full_name'),
            biography=request.form.get('biography'),
            education=request.form.get('education'),
            ordination_details=request.form.get('ordination_details'),
            ministry_experience=request.form.get('ministry_experience'),
            called_to_church_date=called_date,
            leadership_message=request.form.get('leadership_message'),
            pastoral_vision=request.form.get('pastoral_vision'),
            photo_filename=photo_filename
        )


        db.session.add(pastor)
        db.session.commit()


        flash(
            'Pastor Profile created successfully.',
            'success'
        )

        return redirect(
            url_for('pastor_management.create_pastor_profile')
        )


    return render_template(
        'pastor_management/create.html'
    )


@pastor_management_bp.route('/profile', methods=['GET'])
@login_required
@admin_required
def pastor_profile():

    church = ChurchProfile.query.filter_by(
        owner_id=current_user.id
    ).first()


    if not church:
        flash(
            'Please create your Church Profile first.',
            'error'
        )
        return redirect(
            url_for('church_management.create_church_profile')
        )


    pastor = PastorProfile.query.filter_by(
        church_id=church.id
    ).first()


    if not pastor:
        return redirect(
            url_for('pastor_management.create_pastor_profile')
        )


    return render_template(
        'pastor_management/profile.html',
        pastor=pastor
    )
