from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
import uuid
import requests

from modules.content_generator.flyer_engine.layout_engine import FlyerLayout

from .flyer_engine.fonts import load_font
from .flyer_engine.themes import THEMES, detect_flyer_theme
from .flyer_engine.background import (
    create_flyer_canvas,
    add_background_gradient
)
from .flyer_engine.decorations import add_decorative_effects
from .flyer_engine.portraits import (
    resize_image,
    create_portrait
)
from .flyer_engine.speakers import place_speakers
from .flyer_engine.assets import place_assets
from .flyer_engine.logo import (
    add_logo,
    add_footer_branding
)
from .flyer_engine.text import (
    smart_font_size,
    calculate_content_space,
    draw_wrapped_text
)
from .flyer_engine.premium import add_premium_decoration
from .flyer_engine.fal_generator import generate_flyer_background
from .flyer_engine.brand_memory import get_brand_profile
from modules.ai_gateway.gateway import run_ai


# ==============================
# AI FLYER THEME DECISION ENGINE
# ==============================

def detect_flyer_theme(title, current="default"):

    if current != "default":
        return current

    text = title.lower()

    if any(word in text for word in [
        "prayer",
        "fasting",
        "presence",
        "psalm",
        "worship"
    ]):
        return "prayer"

    if any(word in text for word in [
        "revival",
        "power",
        "fire",
        "awakening"
    ]):
        return "revival"

    if any(word in text for word in [
        "youth",
        "teen",
        "camp",
        "young"
    ]):
        return "youth"

    if any(word in text for word in [
        "conference",
        "seminar",
        "leadership",
        "training"
    ]):
        return "conference"

    return "default"

# ==============================
# FLYER THEMES
# ==============================

THEMES = {

    "prayer": {
        "primary": (80, 0, 120),
        "secondary": (255, 215, 0),
        "accent": (255,255,255),
        "overlay": 120,
        "style": "spiritual",
        "text": "white"
    },

    "revival": {
        "primary": (180, 0, 0),
        "secondary": (255, 180, 0),
        "accent": (255,255,255),
        "overlay": 130,
        "style": "fire",
        "text": "white"
    },

    "conference": {
        "primary": (0, 70, 140),
        "secondary": (255,255,255),
        "accent": (0,200,255),
        "overlay": 100,
        "style": "professional",
        "text": "white"
    },

    "youth": {
        "primary": (0,150,100),
        "secondary": (255,215,0),
        "accent": (255,255,255),
        "overlay": 110,
        "style": "modern",
        "text": "white"
    },

    "fasting": {
        "primary": (45,0,90),
        "secondary": (255,215,0),
        "accent": (255,255,255),
        "overlay": 140,
        "style": "deep prayer",
        "text": "white"
    },

    "default": {
        "primary": (20,20,20),
        "secondary": (255,215,0),
        "accent": (255,255,255),
        "overlay": 100,
        "style": "classic",
        "text": "white"
    }

}


# ==============================
# CANVAS CREATOR
# ==============================

# ==============================
# DECORATIVE EFFECT ENGINE
# ==============================

def analyze_event_style(
        title,
        bible_verse="",
        speakers=None
):

    content = (
        title + " " + bible_verse
    ).lower()


    style = {
        "focus": "balanced",
        "speaker_mode": "normal",
        "verse_priority": False,
        "energy": "calm"
    }


    # Prayer events

    if any(word in content for word in [
        "prayer",
        "fasting",
        "presence",
        "altar",
        "seeking"
    ]):

        style["focus"] = "spiritual"
        style["verse_priority"] = True
        style["energy"] = "deep"


    # Revival events

    if any(word in content for word in [
        "revival",
        "fire",
        "power",
        "awakening"
    ]):

        style["focus"] = "revival"
        style["energy"] = "high"


    # Training events

    if any(word in content for word in [
        "conference",
        "seminar",
        "leadership",
        "training"
    ]):

        style["focus"] = "professional"


    # Speaker handling

    if speakers:

        if len(speakers) == 1:
            style["speaker_mode"] = "hero"

        elif len(speakers) >= 4:
            style["speaker_mode"] = "panel"


    return style


# ==============================
# SMART LAYOUT ENGINE
# ==============================


# ==============================
# PREMIUM DECORATION ENGINE V5
# ==============================

def add_premium_decoration(
        flyer,
        theme="default"
):

    config = THEMES.get(
        theme,
        THEMES["default"]
    )

    overlay = Image.new(
        "RGBA",
        flyer.size,
        (0,0,0,0)
    )

    draw = ImageDraw.Draw(
        overlay
    )

    gold = (
        config["secondary"][0],
        config["secondary"][1],
        config["secondary"][2],
        180
    )

    # Elegant border

    draw.rounded_rectangle(
        (
            25,
            25,
            flyer.width-25,
            flyer.height-25
        ),
        radius=35,
        outline=gold,
        width=8
    )


    # Corner ornaments

    size = 80

    corners = [
        (40,40),
        (flyer.width-120,40),
        (40,flyer.height-120),
        (flyer.width-120,flyer.height-120)
    ]


    for x,y in corners:

        draw.arc(
            (
                x,
                y,
                x+size,
                y+size
            ),
            0,
            180,
            fill=gold,
            width=6
        )


    # Light particles

    for i in range(18):

        x = (i*73) % flyer.width
        y = (i*137) % flyer.height

        draw.ellipse(
            (
                x,
                y,
                x+8,
                y+8
            ),
            fill=gold
        )


    overlay = overlay.filter(
        ImageFilter.GaussianBlur(1)
    )


    flyer.alpha_composite(
        overlay
    )


def add_footer_branding(
        flyer,
        theme="default",
        ministry="InChristAlone AI Studio",
        event_type="general",
        church_name=""
):

    config = THEMES.get(
        theme,
        THEMES["default"]
    )

    draw = ImageDraw.Draw(
        flyer
    )

    footer_font = load_font(
        22
    )

    small_font = load_font(
        16
    )

    y = flyer.height - 70

    draw.line(
        (
            80,
            y-15,
            flyer.width-80,
            y-15
        ),
        fill=config["secondary"],
        width=3
    )

    if event_type == "birthday":
        text = "🎉 Celebrating God's Faithfulness"
    else:
        text = ministry

    width = draw.textlength(
        text,
        font=footer_font
    )

    draw.text(
        (
            (flyer.width-width)//2,
            y
        ),
        text,
        font=footer_font,
        fill=config["secondary"]
    )

    if church_name:
        church_width = draw.textlength(
            church_name,
            font=small_font
        )

        draw.text(
            (
                (flyer.width-church_width)//2,
                y+28
            ),
            church_name,
            font=small_font,
            fill=config["accent"]
        )

def generate_flyer_v5(
        title,
        bible_verse="",
        theme="default",
        event_date="",
        venue="",
        speakers=None,
        logo_path=None,
        background_path=None,
        design_settings=None,
        layout=None,
        images=None,
        output_dir="static/generated",
        church_id=None
    ):

    # ==============================
    # AI DESIGN DECISION ENGINE
    # ==============================

    theme = detect_flyer_theme(
        title,
        theme
    )


    # ==============================
    # AI COMPOSITION INTELLIGENCE
    # ==============================

    def analyze_composition(title, speakers):

        title_lower = title.lower()

        if "conference" in title_lower:
            event_type = "conference"

        elif "revival" in title_lower:
            event_type = "revival"

        elif "training" in title_lower:
            event_type = "training"

        elif "worship" in title_lower:
            event_type = "worship"

        else:
            event_type = "general"


        speaker_count = len(
            speakers
            if speakers
            else []
        )


        if speaker_count == 1:
            layout_style = "hero"

        elif speaker_count == 2:
            layout_style = "balanced"

        elif speaker_count == 3:
            layout_style = "triangle"

        else:
            layout_style = "panel"


        return {
            "event_type": event_type,
            "layout_style": layout_style,
            "speaker_count": speaker_count
        }


    composition = analyze_composition(
        title,
        speakers
    )

    # ==============================
    # AI ART DIRECTOR PERSONALITY
    # ==============================

    event_type = composition.get(
        "event_type",
        "general"
    )

    personality_map = {
        "conference": "conference",
        "revival": "revival",
        "training": "conference",
        "worship": "prayer",
        "general": theme
    }

    theme_personality = personality_map.get(
        event_type,
        theme
    )


    if design_settings is None:
        design_settings = {}

    title_color = design_settings.get(
        "title_color",
        "white"
    )

    verse_color = design_settings.get(
        "verse_color",
        "white"
    )

    speaker_name_color = design_settings.get(
        "speaker_name_color",
        "gold"
    )

    def normalize_color(color):
        colors = {
            "white": (255,255,255),
            "black": (0,0,0),
            "gold": (255,215,0),
            "yellow": (255,255,0),
            "blue": (0,120,255),
            "green": (0,200,100),
            "red": (255,60,60)
        }

        if isinstance(color, tuple):
            return color

        if isinstance(color, str):
            return colors.get(
                color.lower(),
                (255,255,255)
            )

        return (255,255,255)

    title_color = normalize_color(title_color)
    verse_color = normalize_color(verse_color)
    speaker_name_color = normalize_color(speaker_name_color)

    speaker_layout = design_settings.get(
        "speaker_layout",
        composition.get(
            "layout_style",
            "bottom"
        )
    )

    # Early visual profile fallback
    visual_profile = {
        "logo_position": "top_left",
        "speaker_priority": "medium",
        "verse_priority": "medium"
    }

    logo_position = design_settings.get(
        "logo_position",
        visual_profile.get(
            "logo_position",
            "top_left"
        )
    )

    title_font_family = design_settings.get(
        "title_font_family",
        "sans"
    )

    verse_font_family = design_settings.get(
        "verse_font_family",
        "serif"
    )

    speaker_font_family = design_settings.get(
        "speaker_font_family",
        "sans"
    )


    brand_profile = None

    if church_id:
        brand_profile = get_brand_profile(
            church_id
        )

    flyer, draw, config = create_flyer_canvas(
        theme=theme_personality,
        brand_profile=brand_profile
    )

    ai_background_loaded = False

    if background_path and os.path.exists(background_path):
        try:
            ai_background = Image.open(background_path).convert("RGBA")
            ai_background = ai_background.resize(flyer.size)
            flyer = ai_background
            draw = ImageDraw.Draw(flyer)
            ai_background_loaded = True
        except Exception:
            pass



    if not ai_background_loaded:

        try:
            fal_background = generate_flyer_background(
                title=title,
                theme=theme_personality,
                event_type="ministry",
                bible_verse=bible_verse,
                church_id=church_id
            )

            if fal_background:

                ai_background = Image.open(
                    requests.get(
                        fal_background,
                        stream=True,
                        timeout=20
                    ).raw
                ).convert("RGBA")

                ai_background = ai_background.resize(
                    flyer.size
                )

                flyer = ai_background
                draw = ImageDraw.Draw(
                    flyer
                )

                ai_background_loaded = True

        except Exception:
            pass


    if not ai_background_loaded:

        add_background_gradient(
            flyer,
            theme_personality
        )

    add_decorative_effects(
        flyer,
        theme_personality
    )


    # ==============================
    # LAYOUT INTELLIGENCE ENGINE
    # ==============================

    layout_engine = FlyerLayout(
        width=flyer.width,
        height=flyer.height,
        speakers=len(speakers or [])
    )


    # ==============================
    # AI ADAPTIVE TITLE SIZE ENGINE
    # ==============================

    if "title_font_size" in design_settings:

        title_font_size = design_settings.get(
            "title_font_size"
        )

    else:

        title_length = len(
            title
        )

        event_type = composition.get(
            "event_type",
            "general"
        )

        # ==============================
        # AI VISUAL HIERARCHY PROFILE
        # ==============================

        hierarchy_profiles = {
            "conference": {
                "title_priority": "high",
                "verse_priority": "medium",
                "speaker_priority": "high",
                "logo_position": "top_left"
            },

            "revival": {
                "title_priority": "high",
                "verse_priority": "very_high",
                "speaker_priority": "medium",
                "logo_position": "top_center"
            },

            "training": {
                "title_priority": "medium",
                "verse_priority": "low",
                "speaker_priority": "high",
                "logo_position": "top_left"
            },

            "worship": {
                "title_priority": "high",
                "verse_priority": "high",
                "speaker_priority": "medium",
                "logo_position": "top_center"
            },

            "general": {
                "title_priority": "medium",
                "verse_priority": "medium",
                "speaker_priority": "medium",
                "logo_position": "top_left"
            }
        }

        visual_profile = hierarchy_profiles.get(
            event_type,
            hierarchy_profiles["general"]
        )

        if event_type == "conference":

            if title_length <= 45:
                title_font_size = 82
            elif title_length <= 70:
                title_font_size = 72
            else:
                title_font_size = 62

        elif event_type == "revival":

            if title_length <= 45:
                title_font_size = 76
            elif title_length <= 70:
                title_font_size = 68
            else:
                title_font_size = 58

        elif event_type == "training":

            if title_length <= 45:
                title_font_size = 70
            elif title_length <= 70:
                title_font_size = 62
            else:
                title_font_size = 54

        else:

            if title_length <= 25:
                title_font_size = 82

            elif title_length <= 45:
                title_font_size = 72

            elif title_length <= 70:
                title_font_size = 62

            else:
                title_font_size = 52


    event_type = composition.get(
        "event_type",
        "general"
    )

    if "verse_font_size" in design_settings:
        verse_font_size = design_settings.get(
            "verse_font_size"
        )

    else:

        verse_priority = visual_profile.get(
            "verse_priority",
            "medium"
        )

        if verse_priority == "very_high":
            verse_font_size = 42

        elif verse_priority == "high":
            verse_font_size = 36

        elif verse_priority == "low":
            verse_font_size = 30

        else:
            verse_font_size = 34


    if "speaker_font_size" in design_settings:
        speaker_font_size = design_settings.get(
            "speaker_font_size"
        )

    else:

        speaker_priority = visual_profile.get(
            "speaker_priority",
            "medium"
        )

        if speaker_priority == "high":
            speaker_font_size = 32

        elif speaker_priority == "low":
            speaker_font_size = 26

        else:
            speaker_font_size = 28
    
    title_font = load_font(
    title_font_size,
    title_font_family
    )
    
    verse_font = load_font(
    verse_font_size,
    verse_font_family
    )
    
    info_font = load_font(
    speaker_font_size,
    speaker_font_family
    )
    
    # ==============================
    # PREMIUM TITLE AREA
    # ==============================

    title_x, title_y = layout_engine.title_position()


    glow = Image.new(
        "RGBA",
        flyer.size,
        (0,0,0,0)
    )

    glow_draw = ImageDraw.Draw(
        glow
    )

    glow_draw.text(
        (
            title_x,
            title_y
        ),
        title,
        font=title_font,
        fill=(
            title_color[0],
            title_color[1],
            title_color[2],
            120
        )
    )

    glow = glow.filter(
        ImageFilter.GaussianBlur(12)
    )

    flyer.alpha_composite(
        glow
    )


    shadow = Image.new(
        "RGBA",
        flyer.size,
        (0,0,0,0)
    )

    shadow_draw = ImageDraw.Draw(
        shadow
    )

    shadow_draw.text(
        (
            title_x+5,
            title_y+8
        ),
        title,
        font=title_font,
        fill=(0,0,0,160)
    )

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(5)
    )

    flyer.alpha_composite(
        shadow
    )


    draw_wrapped_text(
        draw,
        title,
        (
            title_x,
            title_y
        ),
        title_font,
        940,
        title_color
    )


# VERSE PANEL
# ==============================

    verse_x, verse_y = layout_engine.verse_position()

    verse_height = 170

    verse_panel = Image.new(
    "RGBA",
    flyer.size,
    (0,0,0,0)
    )

    verse_draw = ImageDraw.Draw(
    verse_panel
    )

    verse_draw.rounded_rectangle(
    (
        65,
        verse_y-35,
        flyer.width-65,
        verse_y+verse_height-35
    ),
    radius=35,
    fill=(0,0,0,110),
    outline=(
        config["secondary"][0],
        config["secondary"][1],
        config["secondary"][2],
        180
    ),
    width=3
    )

    verse_panel = verse_panel.filter(
    ImageFilter.GaussianBlur(1)
    )

    flyer.alpha_composite(
    verse_panel
    )


    draw_wrapped_text(
        draw,
        bible_verse,
        (verse_x + 20, verse_y),
        verse_font,
        880,
        verse_color
    )


    # ==============================
    # EVENT DETAILS CARD
    # ==============================

    info_x, info_y = layout_engine.event_info_position()

    draw.rounded_rectangle(
        (
            info_x-10,
            info_y,
            flyer.width-60,
            info_y+140
        ),
        radius=25,
        fill=(0,0,0,100)
    )

    draw.text(
        (info_x+20, info_y+25),
        event_date,
        font=info_font,
        fill="white"
    )

    draw.text(
        (info_x+20, info_y+85),
        venue,
        font=info_font,
        fill="white"
    )


    # Speakers

    place_speakers(
          flyer,
          speakers or [],
            theme,
            positions=layout_engine.speaker_position()
      )



    # Event Images

    place_assets(
        flyer,
        images or [],
        theme
    )

    # Logo

    add_logo(
        flyer,
        logo_path,
        logo_position
    )



    footer_event_type = "general"

    title_check = title.lower()

    if (
        "birthday" in title_check
        or "happy birthday" in title_check
        or "celebration" in title_check
    ):
        footer_event_type = "birthday"

    add_footer_branding(
        flyer,
        theme,
        event_type=footer_event_type
    )


    # Premium Decorations

    add_premium_decoration(
        flyer,
        theme
    )


    os.makedirs(
        output_dir,
        exist_ok=True
    )


    filename = (
        "flyer_v4_" +
        str(uuid.uuid4()) +
        ".png"
    )


    path = os.path.join(
        output_dir,
        filename
    )


    flyer.convert(
        "RGB"
    ).save(
        path,
        quality=95
    )


    return path





# ==============================
# AI COMPOSER PIPELINE
# ==============================

def ai_compose_flyer(
        title,
        bible_verse="",
        event_date="",
        venue="",
        speakers=None,
        logo_path=None,
        theme="default",
        background_path=None,
        images=None,
        output_dir="static/generated",
        church_id=None
):

    # ==============================
    # AI GATEWAY FLYER INTELLIGENCE
    # ==============================

    ai_direction = None

    try:
        flyer_prompt = f"""
You are a Christian ministry flyer design assistant.

Create creative direction for this flyer:

Title: {title}
Bible Verse: {bible_verse}
Event Date: {event_date}
Venue: {venue}
Theme: {theme}

Provide:
- recommended visual mood
- colour direction
- design emphasis
- audience feeling

Keep the response concise.
"""

        ai_direction = run_ai(
            prompt=flyer_prompt,
            task="flyer_generation",
            church_id=church_id,
        )

    except Exception as e:
        print("Flyer AI Gateway enhancement failed:", e)

    # AI understanding

    style = analyze_event_style(
        title,
        bible_verse,
        speakers
    )


    # Theme decision

    theme = detect_flyer_theme(
        title,
        theme
    )


    # ==============================
    # AI COMPOSITION INTELLIGENCE
    # ==============================

    def analyze_composition(title, speakers):

        title_lower = title.lower()

        if "conference" in title_lower:
            event_type = "conference"

        elif "revival" in title_lower:
            event_type = "revival"

        elif "training" in title_lower:
            event_type = "training"

        elif "worship" in title_lower:
            event_type = "worship"

        else:
            event_type = "general"


        speaker_count = len(
            speakers
            if speakers
            else []
        )


        if speaker_count == 1:
            layout_style = "hero"

        elif speaker_count == 2:
            layout_style = "balanced"

        elif speaker_count == 3:
            layout_style = "triangle"

        else:
            layout_style = "panel"


        return {
            "event_type": event_type,
            "layout_style": layout_style,
            "speaker_count": speaker_count
        }


    composition = analyze_composition(
        title,
        speakers
    )


    # Layout preparation

    layout = calculate_content_space(
        speakers,
        bible_verse
    )


    # Generate flyer

    flyer_path = generate_flyer_v5(
        title=title,
        bible_verse=bible_verse,
        theme=theme,
        event_date=event_date,
        venue=venue,
        speakers=speakers,
        logo_path=logo_path,
          background_path=background_path,
          layout=layout,
        images=images,
        output_dir=output_dir,
        church_id=church_id
    )


    return {
        "file": flyer_path,
        "theme": theme,
        "style": style,
        "layout": layout
    }


# ==============================
# EXPORT HELPERS
# ==============================

def export_pdf(
        image_path,
        pdf_path
):

    img = Image.open(
        image_path
    ).convert(
        "RGB"
    )


    img.save(
        pdf_path,
        "PDF",
        resolution=100.0
    )
    # ==============================
# ==============================
