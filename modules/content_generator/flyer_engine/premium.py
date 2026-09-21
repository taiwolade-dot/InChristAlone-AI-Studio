from PIL import Image, ImageDraw, ImageFilter

from .themes import THEMES


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
