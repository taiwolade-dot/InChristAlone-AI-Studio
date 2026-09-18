from ..fal_service import generate_image


def build_flyer_visual_prompt(
    title,
    theme="default",
    event_type="general",
    bible_verse=""
):

    prompt = f"""
Create a premium Christian ministry flyer background.

Event:
{title}

Event Type:
{event_type}

Theme:
{theme}

Style:
Professional church media design,
cinematic lighting,
modern worship atmosphere,
high quality,
no text,
no words,
no logos.
"""

    if bible_verse:
        prompt += f"""
Inspirational biblical atmosphere inspired by:
{bible_verse}
"""

    return prompt



def generate_flyer_background(
    title,
    theme="default",
    event_type="general",
    bible_verse=""
):

    prompt = build_flyer_visual_prompt(
        title,
        theme,
        event_type,
        bible_verse
    )

    return generate_image(prompt)
