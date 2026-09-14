from PIL import Image, ImageDraw, ImageFilter
from .themes import THEMES


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
