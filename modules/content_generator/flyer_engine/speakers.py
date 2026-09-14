import os

from PIL import Image, ImageDraw, ImageFilter

from .themes import THEMES
from .fonts import load_font
from .portraits import create_portrait


def place_speakers(
        flyer,
        speakers,
        theme="default",
        speaker_name_color="gold",
        speaker_layout="bottom",
        speaker_y=None,
        positions=None
):

    if not speakers:
        return

    config = THEMES.get(
        theme,
        THEMES["default"]
    )

    width, height = flyer.size

    draw = ImageDraw.Draw(
        flyer
    )

    count = min(
        len(speakers),
        5
    )

    # ==============================
    # AI SPEAKER HIERARCHY ENGINE
    # ==============================

    speaker_profile = []

    for speaker in speakers[:5]:

        role = speaker.get(
            "role",
            ""
        ).lower()

        priority = "normal"

        if any(word in role for word in [
            "pastor",
            "bishop",
            "apostle",
            "host",
            "speaker"
        ]):
            priority = "lead"

        speaker_profile.append({
            "priority": priority
        })

    # ==============================
    # AI HIERARCHY PORTRAIT SCALING
    # ==============================

    lead_exists = any(
        item["priority"] == "lead"
        for item in speaker_profile
    )

    if count == 1:
        portrait_size = 280

    elif count == 2:
        portrait_size = 240

    elif count == 3:

        portrait_size = 220

    else:

        portrait_size = 170

    if lead_exists:
        portrait_size += 20

    if positions is None:

        start_y = (
            speaker_y
            if speaker_y
            else int(height * 0.60)
        )

        positions = []

        if count == 1:
            positions.append(
                (
                    width//2 - portrait_size//2,
                    start_y
                )
            )

        elif count == 2:
            positions = [
                (
                    width//4 - portrait_size//2,
                    start_y
                ),
                (
                    (width*3)//4 - portrait_size//2,
                    start_y
                )
            ]

        elif count == 3:
            positions = [
                (
                    width//2 - portrait_size//2,
                    start_y - 40
                ),
                (
                    width//4 - portrait_size//2,
                    start_y + 80
                ),
                (
                    (width*3)//4 - portrait_size//2,
                    start_y + 80
                )
            ]

        else:
            columns = 2
            for i in range(count):
                row = i // columns
                col = i % columns

                positions.append(
                    (
                        width//4 + col*(width//2) - portrait_size//2,
                        start_y + row*120
                    )
                )

    name_font = load_font(26)
    role_font = load_font(20)

    for index, speaker in enumerate(
        speakers[:5]
    ):

        # ==============================
        # AI LEAD SPEAKER VISUAL PROFILE
        # ==============================

        priority = speaker_profile[index].get(
            "priority",
            "normal"
        )

        if priority == "lead":
            halo_strength = 130
            ring_width = 6
        else:
            halo_strength = 80
            ring_width = 4

        photo = speaker.get(
            "photo",
            ""
        )

        if not os.path.exists(photo):
            continue

        portrait = create_portrait(
            photo,
            portrait_size,
            (
                config["secondary"][0],
                config["secondary"][1],
                config["secondary"][2],
                255
            )
        )

        x,y = positions[index]

        # Premium portrait halo
        glow = Image.new(
            "RGBA",
            (
                portrait.size[0] + 80,
                portrait.size[1] + 80
            ),
            (0,0,0,0)
        )

        glow_draw = ImageDraw.Draw(
            glow
        )

        glow_draw.ellipse(
            (
                20,
                20,
                portrait.size[0] + 60,
                portrait.size[1] + 60
            ),
            fill=(
                config["secondary"][0],
                config["secondary"][1],
                config["secondary"][2],
                halo_strength
            )
        )

        glow_draw.ellipse(
            (
                35,
                35,
                portrait.size[0] + 45,
                portrait.size[1] + 45
            ),
            outline=(
                255,
                255,
                255,
                120
            ),
            width=ring_width
        )

        glow = glow.filter(
            ImageFilter.GaussianBlur(18)
        )

        flyer.alpha_composite(
            glow,
            (x,y)
        )

        flyer.alpha_composite(
            portrait,
            (x,y)
        )

        if portrait_size >= 260:
            card_width = 300
            card_height = 100
        elif portrait_size >= 220:
            card_width = 260
            card_height = 95
        elif portrait_size >= 200:
            card_width = 240
            card_height = 90
        else:
            card_width = 220
            card_height = 85

        # ==============================
        # AI SPEAKER CARD HIERARCHY
        # ==============================

        speaker_priority = speaker_profile[index].get(
            "priority",
            "normal"
        )

        if speaker_priority == "lead":
            card_width += 20
            card_height += 15


        # ==============================
        # AI PREMIUM CARD STYLE PROFILE
        # ==============================

        if speaker_priority == "lead":
            shadow_alpha = 130
            shadow_blur = 18
            border_width = 5
        else:
            shadow_alpha = 90
            shadow_blur = 12
            border_width = 3

        card = Image.new(
            "RGBA",
            (card_width, card_height),
            (0,0,0,110)
        )

        shadow = Image.new(
            "RGBA",
            (card_width + 20, card_height + 20),
            (0,0,0,0)
        )

        shadow_draw = ImageDraw.Draw(
            shadow
        )

        shadow_draw.rounded_rectangle(
            (10,10,card_width+10,card_height+10),
            radius=24,
            fill=(0,0,0,shadow_alpha)
        )

        shadow = shadow.filter(
            ImageFilter.GaussianBlur(shadow_blur)
        )

        card_draw = ImageDraw.Draw(
            card
        )

        card_draw.rounded_rectangle(
            (0,0,card_width,card_height),
            radius=20,
            outline=(
                config["secondary"][0],
                config["secondary"][1],
                config["secondary"][2],
                255
            ),
            width=border_width
        )

        name = speaker.get(
            "name",
            ""
        )

        role = speaker.get(
            "title",
            ""
        )

        name_y = int(card_height * 0.18)
        role_y = int(card_height * 0.55)

        # ==============================
        # AI SPEAKER TYPOGRAPHY HIERARCHY
        # ==============================

        if speaker_priority == "lead":
          card_name_font = load_font(30)
          card_role_font = load_font(22)
        else:
          card_name_font = name_font
          card_role_font = role_font



          card_draw.text(
              (15,name_y),
              name[:24],
              font=card_name_font,
              fill="white"
          )

        card_draw.text(
            (15,role_y),
            role[:28],
            font=card_role_font,
            fill=config["secondary"]
        )

        flyer.alpha_composite(
            shadow,
            (
                x-10,
                y+portrait_size
            )
        )

        flyer.alpha_composite(
            card,
            (
                x,
                y+portrait_size+10
            )
        )


# ==============================
# LOGO HANDLER V4
# ==============================
