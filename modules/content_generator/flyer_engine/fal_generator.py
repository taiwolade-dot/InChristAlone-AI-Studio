from ..fal_service import generate_image
from .event_intelligence import detect_event_type
from .prompts import MINISTRY_VISUAL_PROMPTS
from .brand_memory import get_brand_profile


def build_flyer_visual_prompt(
    title,
    theme="default",
    event_type="general",
    bible_verse="",
    church_id=None
):

    brand = get_brand_profile(
        church_id
    )

    prompt = f"""
Create a premium Christian ministry flyer background.

Event:
{title}

Event Type:
{event_type}

Theme:
{theme}

Visual Direction:
{MINISTRY_VISUAL_PROMPTS.get(event_type, "")}

Church Brand Identity:

Brand Style:
{brand.get("style")}

Tone:
{brand.get("tone")}

Primary Color:
{brand.get("primary_color")}

Accent Color:
{brand.get("accent_color")}

Layout Preference:
{brand.get("layout")}

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
    bible_verse="",
    church_id=None
):

    prompt = build_flyer_visual_prompt(
        title,
        theme,
        event_type,
        bible_verse,
        church_id
    )

    return generate_image(prompt)
