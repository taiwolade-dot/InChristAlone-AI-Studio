from flask import Blueprint, render_template, request
from flask_login import login_required
from .data import PROMPT_CATEGORIES

prompt_engine_bp = Blueprint(
    'prompt_engine',
    __name__,
    url_prefix='/prompt-engine',
    template_folder='../../templates/prompt_engine'
)


@prompt_engine_bp.route('/', methods=['GET'])
@login_required
def index():
    selected_category = request.args.get('category')
    category_data = PROMPT_CATEGORIES.get(selected_category)

    return render_template(
        'prompt_engine/index.html',
        categories=PROMPT_CATEGORIES,
        selected_category=selected_category,
        category_data=category_data,
        generated_prompt=None
    )


@prompt_engine_bp.route('/generate', methods=['POST'])
@login_required
def generate():
    selected_category = request.form.get('category')
    category_data = PROMPT_CATEGORIES.get(selected_category)

    generated_prompt = None
    if category_data:
        values = {
            field: request.form.get(field, '').strip()
            for field in category_data['fields']
        }
        generated_prompt = category_data['template'].format(**values)

    return render_template(
        'prompt_engine/index.html',
        categories=PROMPT_CATEGORIES,
        selected_category=selected_category,
        category_data=category_data,
        generated_prompt=generated_prompt
    )