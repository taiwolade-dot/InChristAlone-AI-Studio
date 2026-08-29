from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
import uuid


# ==============================
# AI THEME SELECTOR
# ==============================

def detect_flyer_theme(
        title="",
        theme="default"
):

    if theme and theme != "default":
        return theme

    content = title.lower()


    if any(word in content for word in [
        "fasting",
        "prayer",
        "intercession",
        "seeking god",
        "presence"
    ]):
        return "fasting"


    if any(word in content for word in [
        "revival",
        "awakening",
        "fire",
        "power"
    ]):
        return "revival"


    if any(word in content for word in [
        "youth",
        "teen",
        "camp",
        "young"
    ]):
        return "youth"


    if any(word in content for word in [
        "conference",
        "seminar",
        "leadership",
        "training"
    ]):
        return "conference"


    return "prayer"




# ==============================
# AI FONT PAIRING ENGINE
# ==============================

def get_ai_font_pairing(theme):
    font_pairs = {
        'fasting': {'title_font_family':'serif', 'verse_font_family':'serif', 'speaker_font_family':'sans'},
        'revival': {'title_font_family':'bold', 'verse_font_family':'serif', 'speaker_font_family':'sans'},
        'youth': {'title_font_family':'bold', 'verse_font_family':'sans', 'speaker_font_family':'sans'},
        'conference': {'title_font_family':'sans', 'verse_font_family':'serif', 'speaker_font_family':'sans'},
        'prayer': {'title_font_family':'serif', 'verse_font_family':'serif', 'speaker_font_family':'sans'}
    }
    return font_pairs.get(theme, font_pairs['prayer'])

# ==============================
# FONT ENGINE
# ==============================

def load_font(size, family="sans"):
    font_map = {
        "sans": [
            "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ],
        "bold": [
            "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        ],
        "serif": [
            "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSerif.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
        ],
        "mono": [
            "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
        ]
    }

    for path in font_map.get(family, font_map["sans"]):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()

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

def create_flyer_canvas(
        width=1080,
        height=1350,
        theme="default"
):

    config = THEMES.get(
        theme,
        THEMES["default"]
    )

    canvas = Image.new(
        "RGBA",
        (width, height),
        config["primary"]
    )

    draw = ImageDraw.Draw(canvas)

    return canvas, draw, config


# ==============================
# BACKGROUND EFFECT
# ==============================

def add_background_gradient(
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

    draw = ImageDraw.Draw(overlay)

    primary = config["primary"]
    secondary = config["secondary"]

    # Vertical gradient
    for y in range(flyer.height):

        ratio = y / flyer.height

        color = (
            int(primary[0]*(1-ratio)+secondary[0]*ratio),
            int(primary[1]*(1-ratio)+secondary[1]*ratio),
            int(primary[2]*(1-ratio)+secondary[2]*ratio),
            255
        )

        draw.line(
            [(0,y),(flyer.width,y)],
            fill=color
        )

    # Artistic glow
    glow = Image.new(
        "RGBA",
        flyer.size,
        (0,0,0,0)
    )

    glow_draw = ImageDraw.Draw(glow)

    cx = flyer.width // 2
    cy = flyer.height // 3

    glow_draw.ellipse(
        (
            cx-350,
            cy-350,
            cx+350,
            cy+350
        ),
        fill=(
            secondary[0],
            secondary[1],
            secondary[2],
            90
        )
    )

    glow = glow.filter(
        ImageFilter.GaussianBlur(80)
    )

    overlay = Image.alpha_composite(
        overlay,
        glow
    )

    # Light rays
    for i in range(8):

        x = i * (flyer.width//8)

        draw.line(
            [
                (cx,0),
                (x,flyer.height)
            ],
            fill=(
                255,
                255,
                255,
                25
            ),
            width=3
        )

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(2)
    )

    flyer.alpha_composite(
        overlay
    )


# ==============================
# IMAGE PROCESSING
# ==============================

def resize_image(
        image_path,
        size
):

    img = Image.open(
        image_path
    ).convert("RGBA")

    img.thumbnail(
        size
    )

    return img# ==============================
# PORTRAIT PROCESSOR V4
# ==============================

def create_portrait(
        image_path,
        size=240,
        border_color=(255,215,0,255)
):

    img = Image.open(
        image_path
    ).convert("RGBA")

    img.thumbnail(
        (size,size)
    )

    canvas = Image.new(
        "RGBA",
        (size,size),
        (0,0,0,0)
    )

    x = (size-img.width)//2
    y = (size-img.height)//2

    canvas.paste(
        img,
        (x,y),
        img
    )

    mask = Image.new(
        "L",
        (size,size),
        0
    )

    mask_draw = ImageDraw.Draw(mask)

    mask_draw.ellipse(
        (0,0,size,size),
        fill=255
    )

    canvas.putalpha(mask)

    # Soft shadow
    shadow = Image.new(
        "RGBA",
        (size+40,size+40),
        (0,0,0,0)
    )

    shadow_draw = ImageDraw.Draw(shadow)

    shadow_draw.ellipse(
        (10,15,size+30,size+35),
        fill=(0,0,0,120)
    )

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(12)
    )

    # Gold glass frame
    frame = Image.new(
        "RGBA",
        (size+30,size+30),
        (0,0,0,0)
    )

    frame_draw = ImageDraw.Draw(frame)

    frame_draw.ellipse(
        (5,5,size+25,size+25),
        outline=border_color,
        width=8
    )

    frame.alpha_composite(
        shadow
    )

    frame.alpha_composite(
        canvas,
        (15,15)
    )

    return frame


# ==============================
# SPEAKER PLACEMENT V4
# ==============================


def place_speakers(
        flyer,
        speakers,
        theme="default",
        speaker_name_color="gold",
        speaker_layout="bottom"
):

    if not speakers:
        return

    config = THEMES.get(
        theme,
        THEMES["default"]
    )

    width, height = flyer.size
    draw = ImageDraw.Draw(flyer)

    count = min(len(speakers), 5)

    # Dynamic sizing with layout control

    if speaker_layout == "side":

        portrait_size = 150
        start_y = 430

        positions = []

        for i in range(count):
            positions.append(
                (
                    70,
                    start_y + (i * 170)
                )
            )

    elif speaker_layout == "center":

        portrait_size = 200
        start_y = int(height * 0.58)

        total_width = count * portrait_size + (count-1)*30
        start_x = (width - total_width)//2

        positions = []

        for i in range(count):
            positions.append(
                (
                    start_x + i*(portrait_size+30),
                    start_y
                )
            )

    else:

        if count == 1:

            portrait_size = 280
            start_y = int(height * 0.56)

            positions = [
                ((width-portrait_size)//2, start_y)
            ]

        elif count == 2:

            portrait_size = 220
            start_y = int(height * 0.60)

            positions = [
                (int(width*0.18), start_y),
                (int(width*0.58), start_y)
            ]

        else:

            portrait_size = 190
            start_y = int(height * 0.61)

            spacing = width // (count+1)

            positions = []

            for i in range(count):
                positions.append(
                    (
                        spacing*(i+1)-portrait_size//2,
                        start_y
                    )
                )

    name_font = load_font(28)
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
# LOGO HANDLER V4
# ==============================

def add_logo(
        flyer,
        logo_path,
        logo_position="top_right"
):

    if not logo_path:
        return


    if not os.path.exists(
        logo_path
    ):
        return


    logo = Image.open(
        logo_path
    ).convert("RGBA")


    logo.thumbnail(
        (180,180)
    )


    shadow = Image.new(
        "RGBA",
        logo.size,
        (0,0,0,120)
    )


    positions = {
        "top_left": (35,35),
        "top_right": (flyer.width-logo.width-45,35),
        "bottom_left": (35,flyer.height-logo.height-45),
        "bottom_right": (flyer.width-logo.width-45,flyer.height-logo.height-45)
    }

    x,y = positions.get(
        logo_position,
        positions["top_right"]
    )

    flyer.alpha_composite(
        shadow,
        (
            x+10,
            y+10
        )
    )

    flyer.alpha_composite(
        logo,
        (
            x,
            y
        )
    )


    flyer.alpha_composite(
        logo,
        (
            flyer.width-logo.width-45,
            35
        )
    )





# ==============================
# AI FLYER INTELLIGENCE ENGINE
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

def smart_font_size(
        text,
        max_size=70,
        min_size=36,
        limit=22
):

    if not text:
        return max_size


    length = len(text)


    if length <= limit:
        return max_size

    reduction = (
        length - limit
    ) * 2


    size = max_size - reduction


    if size < min_size:
        size = min_size


    return size



def calculate_content_space(
        speakers,
        verse
):

    space = {
        "title_y":80,
        "verse_y":280,
        "speaker_y":780
    }


    if speakers and len(speakers) >= 3:

        space["speaker_y"] = 720
        space["verse_y"] = 250


    if len(verse) > 120:

        space["verse_y"] = 230


    return space


# ==============================
# PREMIUM DECORATION ENGINE
# ==============================

def add_premium_decoration(
        flyer,
        theme="default"
):

    config = THEMES.get(
        theme,
        THEMES["default"]
    )

    draw = ImageDraw.Draw(flyer)

    width, height = flyer.size


    # Outer gold frame

    draw.rounded_rectangle(
        (
            25,
            25,
            width-25,
            height-25
        ),
        radius=35,
        outline=config["secondary"],
        width=8
    )


    # Inner soft frame

    draw.rounded_rectangle(
        (
            45,
            45,
            width-45,
            height-45
        ),
        radius=30,
        outline=(
            255,
            255,
            255,
            80
        ),
        width=3
    )


    # Light particles

    particle_layer = Image.new(
        "RGBA",
        flyer.size,
        (0,0,0,0)
    )

    particle_draw = ImageDraw.Draw(
        particle_layer
    )


    positions = [
        (100,150),
        (900,180),
        (150,900),
        (850,1100),
        (500,750)
    ]


    for x,y in positions:

        particle_draw.ellipse(
            (
                x-20,
                y-20,
                x+20,
                y+20
            ),
            fill=(
                config["secondary"][0],
                config["secondary"][1],
                config["secondary"][2],
                70
            )
        )


    particle_layer = particle_layer.filter(
        ImageFilter.GaussianBlur(15)
    )


    flyer.alpha_composite(
        particle_layer
    )


# ==============================
# TEXT WRAPPING ENGINE V4
# ==============================

def draw_wrapped_text(
        draw,
        text,
        position,
        font,
        max_width,
        fill="white",
        spacing=10
):

    if not text:
        return


    words = text.split()

    lines = []

    current = ""


    for word in words:

        test = current + " " + word

        if draw.textlength(
            test,
            font=font
        ) <= max_width:

            current = test.strip()

        else:

            if current:
                lines.append(
                    current
                )

            current = word


    if current:
        lines.append(
            current
        )


    x,y = position


    for line in lines:

        draw.text(
            (x,y),
            line,
            font=font,
            fill=fill
        )

        y += font.size + spacing



# ==============================
# MAIN FLYER GENERATOR V4
# ==============================

def generate_flyer_v5(
        title,
        bible_verse="",
        theme="default",
        event_date="",
        venue="",
        speakers=None,
        logo_path=None,
        design_settings=None,
        output_dir="static/generated"
):

    # ==============================
    # AI DESIGN DECISION ENGINE
    # ==============================

    theme = detect_flyer_theme(
        title,
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

    speaker_layout = design_settings.get(
        "speaker_layout",
        "bottom"
    )

    logo_position = design_settings.get(
        "logo_position",
        "top_left"
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


    flyer, draw, config = create_flyer_canvas(
        theme=theme
    )


    add_background_gradient(
        flyer,
        theme
    )


    title_font_size = design_settings.get(
        "title_font_size",
        70
    )

    verse_font_size = design_settings.get(
        "verse_font_size",
        34
    )

    speaker_font_size = design_settings.get(
        "speaker_font_size",
        28
    )
    
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

    shadow = Image.new(
        "RGBA",
        flyer.size,
        (0,0,0,0)
    )

    shadow_draw = ImageDraw.Draw(shadow)

    shadow_draw.text(
        (75,85),
        title,
        font=title_font,
        fill=(0,0,0,150)
    )

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(6)
    )

    flyer.alpha_composite(shadow)

    draw_wrapped_text(
        draw,
        title,
        (70,80),
        title_font,
        940,
        title_color
    )


    # ==============================
    # VERSE PANEL
    # ==============================

    panel = Image.new(
        "RGBA",
        (950,150),
        (0,0,0,90)
    )

    flyer.alpha_composite(
        panel,
        (65,260)
    )

    draw_wrapped_text(
        draw,
        bible_verse,
        (90,290),
        verse_font,
        880,
        verse_color
    )


    # ==============================
    # EVENT DETAILS CARD
    # ==============================

    draw.rounded_rectangle(
        (60,450,1020,590),
        radius=25,
        fill=(0,0,0,100)
    )

    draw.text(
        (90,475),
        event_date,
        font=info_font,
        fill="white"
    )

    draw.text(
        (90,535),
        venue,
        font=info_font,
        fill="white"
    )


    # Speakers

    place_speakers(
        flyer,
        speakers or [],
        theme,
        speaker_name_color,
        speaker_layout
    )


    # Logo

    add_logo(
        flyer,
        logo_path,
        logo_position
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
        output_dir="static/generated"
):

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
        output_dir=output_dir
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
    # PREMIUM TITLE AREA
    # ==============================

    shadow = Image.new(
        "RGBA",
        flyer.size,
        (0,0,0,0)
    )

    shadow_draw = ImageDraw.Draw(shadow)

    shadow_draw.text(
        (75,85),
        title,
        font=title_font,
        fill=(0,0,0,150)
    )

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(6)
    )

    flyer.alpha_composite(shadow)

    draw_wrapped_text(
        draw,
        title,
        (70,80),
        title_font,
        940,
        title_color
    )


    # ==============================
    # VERSE PANEL
    # ==============================

    panel = Image.new(
        "RGBA",
        (950,150),
        (0,0,0,90)
    )

    flyer.alpha_composite(
        panel,
        (65,260)
    )

    draw_wrapped_text(
        draw,
        bible_verse,
        (90,290),
        verse_font,
        880,
        verse_color
    )


    # ==============================
    # EVENT DETAILS CARD
    # ==============================

    draw.rounded_rectangle(
        (60,450,1020,590),
        radius=25,
        fill=(0,0,0,100)
    )

    draw.text(
        (90,475),
        event_date,
        font=info_font,
        fill="white"
    )

    draw.text(
        (90,535),
        venue,
        font=info_font,
        fill="white"
    )


    # Speakers

    place_speakers(
        flyer,
        speakers or [],
        theme,
        speaker_name_color,
        speaker_layout
    )


    # Logo

    add_logo(
        flyer,
        logo_path,
        logo_position
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
        output_dir="static/generated"
):

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
        output_dir=output_dir
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
