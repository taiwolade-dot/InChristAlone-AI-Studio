from flask import Blueprint, render_template, request
from flask_login import login_required

from .data import RESEARCH_PROMPTS, CITATION_STYLES
from .citation import format_citation, SOURCE_TYPE_FIELDS, SOURCE_TYPE_LABELS
from modules.wallet_utils import spend_units

research_assistant_bp = Blueprint(
    'research_assistant',
    __name__,
    url_prefix='/research-assistant',
    template_folder='../../templates/research_assistant'
)


@research_assistant_bp.route('/', methods=['GET'])
@login_required
def index():
    active_tab = request.args.get('tab', 'prompts')
    selected_prompt = request.args.get('prompt_category')
    prompt_data = RESEARCH_PROMPTS.get(selected_prompt)

    selected_source_type = request.args.get('source_type')
    source_fields = SOURCE_TYPE_FIELDS.get(selected_source_type)

    return render_template(
        'research_assistant/index.html',
        active_tab=active_tab,
        prompt_categories=RESEARCH_PROMPTS,
        selected_prompt=selected_prompt,
        prompt_data=prompt_data,
        generated_prompt=None,
        citation_styles=CITATION_STYLES,
        source_type_labels=SOURCE_TYPE_LABELS,
        selected_source_type=selected_source_type,
        source_fields=source_fields,
        generated_citation=None
    )


@research_assistant_bp.route('/generate-prompt', methods=['POST'])
@login_required
def generate_prompt():
    result = spend_units(5)
    if result is not True:
        return result

    selected_prompt = request.form.get('prompt_category')
    prompt_data = RESEARCH_PROMPTS.get(selected_prompt)

    generated_prompt = None
    if prompt_data:
        values = {
            field: request.form.get(field, '').strip()
            for field in prompt_data['fields']
        }
        generated_prompt = prompt_data['template'].format(**values)

    return render_template(
        'research_assistant/index.html',
        active_tab='prompts',
        prompt_categories=RESEARCH_PROMPTS,
        selected_prompt=selected_prompt,
        prompt_data=prompt_data,
        generated_prompt=generated_prompt,
        citation_styles=CITATION_STYLES,
        source_type_labels=SOURCE_TYPE_LABELS,
        selected_source_type=None,
        source_fields=None,
        generated_citation=None
    )


@research_assistant_bp.route('/generate-citation', methods=['POST'])
@login_required
def generate_citation():
    result = spend_units(5)
    if result is not True:
        return result

    style = request.form.get('citation_style')
    source_type = request.form.get('source_type')
    fields = SOURCE_TYPE_FIELDS.get(source_type, [])

    field_data = {field: request.form.get(field, '').strip() for field in fields}
    generated_citation = format_citation(style, source_type, field_data)

    return render_template(
        'research_assistant/index.html',
        active_tab='citations',
        prompt_categories=RESEARCH_PROMPTS,
        selected_prompt=None,
        prompt_data=None,
        generated_prompt=None,
        citation_styles=CITATION_STYLES,
        source_type_labels=SOURCE_TYPE_LABELS,
        selected_source_type=source_type,
        source_fields=fields,
        generated_citation=generated_citation
    )