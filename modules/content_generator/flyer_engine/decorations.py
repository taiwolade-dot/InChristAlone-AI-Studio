from PIL import Image, ImageDraw, ImageFilter
from .themes import THEMES


def add_decorative_effects(
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


    # ==========================
    # PREMIUM BORDER FRAME
    # ==========================

    draw.rounded_rectangle(
        (
            25,
            25,
            flyer.width-25,
            flyer.height-25
        ),
        radius=35,
        outline=(
            config["secondary"][0],
            config["secondary"][1],
            config["secondary"][2],
            220
        ),
        width=6
    )


    # ==========================
    # BOKEH LIGHT PARTICLES
    # ==========================

    particles = [
        (120,180,50),
        (900,220,35),
        (180,700,45),
        (850,850,60),
        (500,1100,40),
        (300,350,25),
        (760,500,30)
    ]


    for x,y,size in particles:

        draw.ellipse(
            (
                x-size,
                y-size,
                x+size,
                y+size
            ),
            fill=(
                config["secondary"][0],
                config["secondary"][1],
                config["secondary"][2],
                70
            )
        )


    # ==========================
    # CORNER ORNAMENTS
    # ==========================

    draw.arc(
        (40,40,220,220),
        180,
        270,
        fill=config["secondary"],
        width=6
    )


    draw.arc(
        (
            flyer.width-220,
            flyer.height-220,
            flyer.width-40,
            flyer.height-40
        ),
        0,
        90,
        fill=config["secondary"],
        width=6
    )


    # Soft atmosphere

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(10)
    )


    flyer.alpha_composite(
        overlay
    )


# ==============================
# IMAGE PROCESSING
# ==============================
