import io
import zipfile

from flask import Blueprint, render_template, request, send_file
from flask_login import login_required

from .data import SITE_TYPES, COLOR_SCHEMES
from .generator import build_html, build_css, build_js
from modules.wallet_utils import spend_units

website_generator_bp = Blueprint(
    'website_generator',
    __name__,
    url_prefix='/website-generator',
    template_folder='../../templates/website_generator'
)


@website_generator_bp.route('/', methods=['GET'])
@login_required
def index():
    selected_type = request.args.get('site_type')
    type_data = SITE_TYPES.get(selected_type)

    return render_template(
        'website_generator/index.html',
        site_types=SITE_TYPES,
        color_schemes=COLOR_SCHEMES,
        selected_type=selected_type,
        type_data=type_data
    )

@website_generator_bp.route('/generate', methods=['POST'])
@login_required
def generate():
    result = spend_units(20)
    if result is not True:
        return result

    site_type_key = request.form.get('site_type')
    color_scheme_key = request.form.get('color_scheme', 'royal_blue_gold')
    type_data = SITE_TYPES.get(site_type_key)

    if not type_data:
        return "Invalid site type selected.", 400

    form_data = {
        field: request.form.get(field, '').strip()
        for field in type_data['fields']
    }

    html_content = build_html(site_type_key, form_data, color_scheme_key)
    css_content = build_css(color_scheme_key)
    js_content = build_js()

    # Build ZIP in memory
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('index.html', html_content)
        zf.writestr('style.css', css_content)
        zf.writestr('script.js', js_content)
    memory_file.seek(0)

    site_name = form_data.get('church_name') or form_data.get('ministry_name') or 'website'
    safe_name = "".join(c if c.isalnum() else "_" for c in site_name).strip("_") or "website"

    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'{safe_name}.zip'
    )