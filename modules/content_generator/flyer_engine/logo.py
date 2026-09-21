import os

from PIL import Image, ImageDraw, ImageFilter

from .themes import THEMES
from .fonts import load_font


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







# ==============================
# FOOTER BRANDING ENGINE
# ==============================

def add_footer_branding(
        flyer,
        theme="default",
        ministry="InChristAlone AI Studio",
        church=""
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

    footer_height = 120

    y = flyer.height - footer_height - 20

    draw.rounded_rectangle(
        (
            60,
            y,
            flyer.width-60,
            flyer.height-40
        ),
        radius=30,
        fill=(0,0,0,130)
    )

    draw.line(
        (
            90,
            y+15,
            flyer.width-90,
            y+15
        ),
        fill=(
            config["secondary"][0],
            config["secondary"][1],
            config["secondary"][2],
            255
        ),
        width=3
    )

    church_font = load_font(24)
    brand_font = load_font(20)

    if church:

        church_width = draw.textlength(
            church,
            font=church_font
        )

        draw.text(
            (
                (flyer.width-church_width)//2,
                y+30
            ),
            church,
            font=church_font,
            fill="white"
        )


    brand_width = draw.textlength(
        ministry,
        font=brand_font
    )

    draw.text(
        (
            (flyer.width-brand_width)//2,
            y+65
        ),
        ministry,
        font=brand_font,
        fill=(
            config["secondary"][0],
            config["secondary"][1],
            config["secondary"][2]
        )
    )


    overlay = overlay.filter(
        ImageFilter.GaussianBlur(1)
    )

    flyer.alpha_composite(
        overlay
    )


# ==============================
# AI FLYER INTELLIGENCE ENGINE
# ==============================
