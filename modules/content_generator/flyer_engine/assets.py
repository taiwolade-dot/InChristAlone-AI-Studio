import os
from PIL import Image, ImageDraw, ImageFilter


from .themes import THEMES


def create_asset_card(
    image_path,
    size,
    border_color
):
    img = Image.open(
        image_path
    ).convert("RGBA")

    img.thumbnail(
        size
    )

    canvas = Image.new(
        "RGBA",
        size,
        (0,0,0,0)
    )

    x = (size[0] - img.width)//2
    y = (size[1] - img.height)//2

    canvas.paste(
        img,
        (x,y),
        img
    )

    mask = Image.new(
        "L",
        size,
        0
    )

    mask_draw = ImageDraw.Draw(
        mask
    )

    mask_draw.rounded_rectangle(
        (0,0,size[0],size[1]),
        radius=35,
        fill=255
    )

    canvas.putalpha(
        mask
    )


    shadow = Image.new(
        "RGBA",
        (size[0]+40,size[1]+40),
        (0,0,0,0)
    )

    shadow_draw = ImageDraw.Draw(
        shadow
    )

    shadow_draw.rounded_rectangle(
        (15,15,size[0]+25,size[1]+25),
        radius=35,
        fill=(0,0,0,120)
    )

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(12)
    )


    frame = Image.new(
        "RGBA",
        (size[0]+20,size[1]+20),
        (0,0,0,0)
    )

    frame_draw = ImageDraw.Draw(
        frame
    )

    frame_draw.rounded_rectangle(
        (5,5,size[0]+15,size[1]+15),
        radius=35,
        outline=border_color,
        width=6
    )

    frame.alpha_composite(
        shadow
    )

    frame.alpha_composite(
        canvas,
        (10,10)
    )

    return frame



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

        path = (
            item.get("path")
            if isinstance(item, dict)
            else item
        )

        if path and os.path.exists(path):
            valid_images.append(path)


    if not valid_images:
        return


    border_color = (
        config["secondary"][0],
        config["secondary"][1],
        config["secondary"][2],
        255
    )


    count = min(
        len(valid_images),
        3
    )


    if count == 1:

        card = create_asset_card(
            valid_images[0],
            (520,360),
            border_color
        )

        flyer.alpha_composite(
            card,
            (
                (width-card.width)//2,
                180
            )
        )


    else:

        positions = [
            (70,220),
            (width-330,220),
            (width//2-130,430)
        ]


        for index,path in enumerate(
            valid_images[:3]
        ):

            card = create_asset_card(
                path,
                (240,240),
                border_color
            )


            flyer.alpha_composite(
                card,
                positions[index]
            )
