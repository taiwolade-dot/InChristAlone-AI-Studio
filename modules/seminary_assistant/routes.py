import os
import uuid
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required
from werkzeug.utils import secure_filename
from modules.wallet_utils import spend_units

from models import db, AcademicWork, AcademicDocument
from .data import TOPIC_REFINEMENT_PROMPTS, WORK_TYPES, WORK_STATUSES

seminary_assistant_bp = Blueprint(
    'seminary_assistant',
    __name__,
    url_prefix='/seminary-assistant',
    template_folder='../../templates/seminary_assistant'
)

UPLOAD_FOLDER = os.path.join('uploads', 'thesis')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}


def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _ensure_upload_folder():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@seminary_assistant_bp.route('/', methods=['GET'])
@login_required
def index():
    active_tab = request.args.get('tab', 'my_work')
    filter_type = request.args.get('work_type', '')

    query = AcademicWork.query
    if filter_type:
        query = query.filter_by(work_type=filter_type)
    works = query.order_by(AcademicWork.order, AcademicWork.created_at).all()

    selected_prompt = request.args.get('prompt_category')
    prompt_data = TOPIC_REFINEMENT_PROMPTS.get(selected_prompt)

    return render_template(
        'seminary_assistant/index.html',
        active_tab=active_tab,
        works=works,
        work_types=WORK_TYPES,
        work_statuses=WORK_STATUSES,
        filter_type=filter_type,
        prompt_categories=TOPIC_REFINEMENT_PROMPTS,
        selected_prompt=selected_prompt,
        prompt_data=prompt_data,
        generated_prompt=None
    )

@seminary_assistant_bp.route('/generate-topic-prompt', methods=['POST'])
@login_required
def generate_topic_prompt():
    result = spend_units(5)
    if result is not True:
        return result

    selected_prompt = request.form.get('prompt_category')
    prompt_data = TOPIC_REFINEMENT_PROMPTS.get(selected_prompt)

    generated_prompt = None
    if prompt_data:
        values = {
            field: request.form.get(field, '').strip()
            for field in prompt_data['fields']
        }
        generated_prompt = prompt_data['template'].format(**values)

    works = AcademicWork.query.order_by(AcademicWork.order, AcademicWork.created_at).all()

    return render_template(
        'seminary_assistant/index.html',
        active_tab='topic_refinement',
        works=works,
        work_types=WORK_TYPES,
        work_statuses=WORK_STATUSES,
        filter_type='',
        prompt_categories=TOPIC_REFINEMENT_PROMPTS,
        selected_prompt=selected_prompt,
        prompt_data=prompt_data,
        generated_prompt=generated_prompt
    )


@seminary_assistant_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_work():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        work_type = request.form.get('work_type', 'thesis_chapter')
        status = request.form.get('status', 'not_started')
        deadline_str = request.form.get('deadline', '').strip()
        notes = request.form.get('notes', '').strip()

        if not title:
            flash('Title is required.', 'error')
            return redirect(url_for('seminary_assistant.add_work'))

        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        new_work = AcademicWork(
            title=title,
            work_type=work_type,
            status=status,
            deadline=deadline,
            notes=notes
        )
        db.session.add(new_work)
        db.session.commit()

        flash(f'"{title}" added successfully.', 'success')
        return redirect(url_for('seminary_assistant.index'))

    return render_template('seminary_assistant/add_work.html', work_types=WORK_TYPES, work_statuses=WORK_STATUSES)
@seminary_assistant_bp.route('/work/<int:work_id>', methods=['GET'])
@login_required
def work_detail(work_id):
    work = AcademicWork.query.get_or_404(work_id)
    return render_template('seminary_assistant/work_detail.html', work=work, work_statuses=WORK_STATUSES)


@seminary_assistant_bp.route('/work/<int:work_id>/update-status', methods=['POST'])
@login_required
def update_status(work_id):
    work = AcademicWork.query.get_or_404(work_id)
    work.status = request.form.get('status', work.status)
    db.session.commit()
    flash('Status updated.', 'success')
    return redirect(url_for('seminary_assistant.work_detail', work_id=work_id))


@seminary_assistant_bp.route('/work/<int:work_id>/delete', methods=['POST'])
@login_required
def delete_work(work_id):
    work = AcademicWork.query.get_or_404(work_id)
    title = work.title

    for doc in work.documents:
        file_path = os.path.join(UPLOAD_FOLDER, doc.filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    db.session.delete(work)
    db.session.commit()
    flash(f'"{title}" removed.', 'info')
    return redirect(url_for('seminary_assistant.index'))


@seminary_assistant_bp.route('/work/<int:work_id>/upload', methods=['POST'])
@login_required
def upload_document(work_id):
    work = AcademicWork.query.get_or_404(work_id)

    if 'document' not in request.files:
        flash('No file selected.', 'error')
        return redirect(url_for('seminary_assistant.work_detail', work_id=work_id))

    file = request.files['document']
    if file.filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('seminary_assistant.work_detail', work_id=work_id))

    if not _allowed_file(file.filename):
        flash('File type not allowed. Use PDF, DOC, DOCX, or TXT.', 'error')
        return redirect(url_for('seminary_assistant.work_detail', work_id=work_id))

    _ensure_upload_folder()

    original_filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
    file.save(os.path.join(UPLOAD_FOLDER, unique_filename))

    new_doc = AcademicDocument(
        work_id=work.id,
        filename=unique_filename,
        original_filename=original_filename
    )
    db.session.add(new_doc)
    db.session.commit()

    flash(f'{original_filename} uploaded successfully.', 'success')
    return redirect(url_for('seminary_assistant.work_detail', work_id=work_id))


@seminary_assistant_bp.route('/download/<int:doc_id>', methods=['GET'])
@login_required
def download_document(doc_id):
    doc = AcademicDocument.query.get_or_404(doc_id)
    return send_from_directory(
        os.path.abspath(UPLOAD_FOLDER),
        doc.filename,
        as_attachment=True,
        download_name=doc.original_filename
    )


@seminary_assistant_bp.route('/document/<int:doc_id>/delete', methods=['POST'])
@login_required
def delete_document(doc_id):
    doc = AcademicDocument.query.get_or_404(doc_id)
    work_id = doc.work_id
    file_path = os.path.join(UPLOAD_FOLDER, doc.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.session.delete(doc)
    db.session.commit()
    flash('Document removed.', 'info')
    return redirect(url_for('seminary_assistant.work_detail', work_id=work_id))