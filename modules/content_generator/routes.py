from flask import Blueprint, render_template, request
from flask_login import login_required
from modules.wallet_utils import spend_units
from .data import CONTENT_TYPES

content_generator_bp = Blueprint(
    'content_generator',
    __name__,
    url_prefix='/content-generator',
    template_folder='../../templates/content_generator'
)


def generate_image_from_prompt(prompt_text):
    """
    PLACEHOLDER for future real image generation (e.g. OpenAI DALL-E, Stability AI).

    Once an API key is available, this function should:
    1. Call the image generation API with `prompt_text`
    2. Return the image URL or binary data

    For now, it returns None, and the app falls back to showing the
    generated prompt as text for manual use in an external AI tool.
    """
    return None


@content_generator_bp.route('/', methods=['GET'])
@login_required
def index():
    active_type = request.args.get('type', 'cartoon')
    type_data = CONTENT_TYPES.get(active_type)

    return render_template(
        'content_generator/index.html',
        content_types=CONTENT_TYPES,
        active_type=active_type,
        type_data=type_data,
        generated_prompt=None,
        generated_image_url=None
    )

@content_generator_bp.route('/generate', methods=['POST'])
@login_required
def generate():
    result = spend_units(10)
    if result is not True:
        return result

    content_type = request.form.get('content_type')
    type_data = CONTENT_TYPES.get(content_type)

    generated_prompt = None
    generated_image_url = None

    if type_data:
        values = {
            field: request.form.get(field, '').strip()
            for field in type_data['fields']
        }
        generated_prompt = type_data['template'].format(**values)

        # Only cartoon/flyer are image-based — try real generation if available
        if content_type in ('cartoon', 'flyer'):
            generated_image_url = generate_image_from_prompt(generated_prompt)

    return render_template(
        'content_generator/index.html',
        content_types=CONTENT_TYPES,
        active_type=content_type,
        type_data=type_data,
        generated_prompt=generated_prompt,
        generated_image_url=generated_image_url
    )