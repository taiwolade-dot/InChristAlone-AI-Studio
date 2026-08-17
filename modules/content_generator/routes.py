from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from modules.wallet_utils import spend_units, refund_units
from .data import CONTENT_TYPES
from .fal_service import generate_image, upscale_image, edit_image, generate_video, generate_music, generate_voice, transcribe_audio

content_generator_bp = Blueprint(
    'content_generator',
    __name__,
    url_prefix='/content-generator',
    template_folder='../../templates/content_generator'
)


def generate_image_from_prompt(prompt_text):
    print(">>> generate_image_from_prompt CALLED")
    """
    Calls fal.ai (Flux Schnell) to generate a real image from the prompt text.
    Returns an image URL on success, or None on failure - the template
    falls back to showing the text prompt if this returns None.
    """
    return generate_image(prompt_text)


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
    content_type = request.form.get('content_type')
    unit_cost = 10

    result = spend_units(unit_cost)
    if result is not True:
        return result

    type_data = CONTENT_TYPES.get(content_type)

    generated_prompt = None
    generated_image_url = None
    generated_video_url = None

    if type_data:
        values = {
            field: request.form.get(field, '').strip()
            for field in type_data['fields']
        }
        generated_prompt = type_data['template'].format(**values)

        if content_type in ('cartoon', 'flyer'):
            generated_image_url = generate_image_from_prompt(generated_prompt)
            print("IMAGE URL =", repr(generated_image_url))
            if not generated_image_url:
                refund_units(unit_cost)
                flash(f'Image generation failed. Your {unit_cost} Units have been refunded.', 'error')

    return render_template(
        'content_generator/index.html',
        content_types=CONTENT_TYPES,
        active_type=content_type,
        type_data=type_data,
        generated_prompt=generated_prompt,
        generated_image_url=generated_image_url,
        generated_video_url=generated_video_url
    )

@content_generator_bp.route('/upscale', methods=['POST'])
@login_required
def upscale():
    from modules.wallet_utils import spend_units, refund_units

    result = spend_units(3)
    if result is not True:
        return result

    image_url = request.form.get('image_url')
    active_type = request.form.get('active_type', 'cartoon')

    upscaled_url = None
    if image_url:
        upscaled_url = upscale_image(image_url)
        if not upscaled_url:
            refund_units(3)
            flash('Upscaling failed. Your 3 Units have been refunded.', 'error')

    type_data = CONTENT_TYPES.get(active_type)

    return render_template(
        'content_generator/index.html',
        content_types=CONTENT_TYPES,
        active_type=active_type,
        type_data=type_data,
        generated_prompt=None,
        generated_image_url=upscaled_url or image_url
    )

@content_generator_bp.route('/edit-image', methods=['GET'])
@login_required
def edit_image_form():
    return render_template('content_generator/edit_image.html', edited_image_url=None)


@content_generator_bp.route('/edit-image/submit', methods=['POST'])
@login_required
def edit_image_submit():
    from modules.wallet_utils import spend_units, refund_units
    import base64

    result = spend_units(8)
    if result is not True:
        return result

    edit_prompt = request.form.get('edit_prompt', '').strip()

    if 'photo' not in request.files or request.files['photo'].filename == '':
        flash('Please select a photo to edit.', 'error')
        return redirect(url_for('content_generator.edit_image_form'))

    photo = request.files['photo']
    photo_bytes = photo.read()
    mime_type = photo.mimetype or 'image/jpeg'
    b64_data = base64.b64encode(photo_bytes).decode('utf-8')
    data_uri = f"data:{mime_type};base64,{b64_data}"

    edited_url = edit_image(data_uri, edit_prompt)

    if not edited_url:
        flash('Image editing failed. Please try again.', 'error')
        return redirect(url_for('content_generator.edit_image_form'))

    return render_template('content_generator/edit_image.html', edited_image_url=edited_url)


@content_generator_bp.route('/generate-video', methods=['POST'])
@login_required
def generate_video_route():
    result = spend_units(250)
    if result is not True:
        return result

    edited_script = request.form.get('edited_script', '').strip()

    generated_video_url = None
    if edited_script:
        generated_video_url = generate_video(edited_script)

    return render_template(
        'content_generator/index.html',
        content_types=CONTENT_TYPES,
        active_type='video',
        type_data=CONTENT_TYPES.get('video'),
        generated_prompt=edited_script,
        generated_image_url=None,
        generated_video_url=generated_video_url
    )


@content_generator_bp.route('/generate-music', methods=['POST'])
@login_required
def generate_music_route():
    result = spend_units(15)
    if result is not True:
        return result

    style_prompt = request.form.get('style_prompt', '').strip()
    lyrics = request.form.get('lyrics', '').strip()

    generated_audio_url = None
    if style_prompt and lyrics:
        generated_audio_url = generate_music(style_prompt, lyrics)
        if not generated_audio_url:
            flash("Song generation failed. Check that Style and Lyrics are filled in properly.", "error")

    return render_template(
        'content_generator/index.html',
        content_types=CONTENT_TYPES,
        active_type='music',
        type_data=CONTENT_TYPES.get('music'),
        generated_prompt=None,
        generated_image_url=None,
        generated_video_url=None,
        generated_audio_url=generated_audio_url
    )


@content_generator_bp.route('/voice', methods=['GET'])
@login_required
def voice_form():
    return render_template('content_generator/voice.html', generated_voice_url=None)


@content_generator_bp.route('/voice/submit', methods=['POST'])
@login_required
def voice_submit():
    result = spend_units(20)
    if result is not True:
        return result

    text = request.form.get('text', '').strip()
    voice = request.form.get('voice', 'af_heart')

    generated_voice_url = None
    if text:
        generated_voice_url = generate_voice(text, voice)
        if not generated_voice_url:
            flash("Voice generation failed. Please try again.", "error")

    return render_template('content_generator/voice.html', generated_voice_url=generated_voice_url)


@content_generator_bp.route('/transcribe', methods=['GET'])
@login_required
def transcribe_form():
    return render_template('content_generator/transcribe.html', transcribed_text=None)


@content_generator_bp.route('/transcribe/submit', methods=['POST'])
@login_required
def transcribe_submit():
    import base64

    result = spend_units(10)
    if result is not True:
        return result

    if 'audio_file' not in request.files or request.files['audio_file'].filename == '':
        flash('Please select an audio file.', 'error')
        return redirect(url_for('content_generator.transcribe_form'))

    audio_file = request.files['audio_file']
    audio_bytes = audio_file.read()
    mime_type = audio_file.mimetype or 'audio/mpeg'
    b64_data = base64.b64encode(audio_bytes).decode('utf-8')
    data_uri = f"data:{mime_type};base64,{b64_data}"

    transcribed_text = transcribe_audio(data_uri)

    if not transcribed_text:
        flash('Transcription failed. Please try again.', 'error')

    return render_template('content_generator/transcribe.html', transcribed_text=transcribed_text)
