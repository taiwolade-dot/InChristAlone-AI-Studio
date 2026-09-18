import os
from PIL import Image, ImageDraw, ImageFilter
from .themes import THEMES
from .portraits import resize_image


def place_assets(
    flyer,
    images,
    theme="default"
):
    if not images:
        return

    config = THEMES.get(
        theme,
        THEMES["default"]
    )

    width, height = flyer.size

    valid_images = []

    for item in images:
        path = item.get("path") if isinstance(item, dict) else item

        if path and os.path.exists(path):
            valid_images.append(path)

    if not valid_images:
        return

    draw = ImageDraw.Draw(flyer)

    count = min(len(valid_images), 3)

    if count == 1:
        img = Image.open(
            valid_images[0]
        ).convert("RGBA")

        img.thumbnail(
            (500, 350)
        )

        x = (width - img.width) // 2
        y = 180

        flyer.alpha_composite(
            img,
            (x, y)
        )

    else:
        positions = [
            (80, 220),
            (width - 300, 220),
            (width//2 - 120, 420)
        ]

        for index, path in enumerate(valid_images[:3]):

            img = Image.open(
                path
            ).convert("RGBA")

            img.thumbnail(
                (220,220)
            )

            x, y = positions[index]

            flyer.alpha_composite(
                img,
                (x,y)
            )
