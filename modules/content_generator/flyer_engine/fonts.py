from PIL import ImageFont
import os


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
