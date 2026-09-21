from PIL import ImageDraw


from .fonts import load_font


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
