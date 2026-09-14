from PIL import Image, ImageDraw, ImageFilter


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
