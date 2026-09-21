# ==============================
# FLYER THEME ENGINE
# ==============================

# ==============================
# AI FLYER THEME DECISION ENGINE
# ==============================

def detect_flyer_theme(title, current="default"):

    if current != "default":
        return current

    text = title.lower()

    if any(word in text for word in [
        "prayer",
        "fasting",
        "presence",
        "psalm",
        "worship"
    ]):
        return "prayer"

    if any(word in text for word in [
        "revival",
        "power",
        "fire",
        "awakening"
    ]):
        return "revival"

    if any(word in text for word in [
        "youth",
        "teen",
        "camp",
        "young"
    ]):
        return "youth"

    if any(word in text for word in [
        "conference",
        "seminar",
        "leadership",
        "training"
    ]):
        return "conference"

    return "default"

# ==============================
# FLYER THEMES
# ==============================

THEMES = {

    "prayer": {
        "primary": (80, 0, 120),
        "secondary": (255, 215, 0),
        "accent": (255,255,255),
        "overlay": 120,
        "style": "spiritual",
        "text": "white"
    },

    "revival": {
        "primary": (180, 0, 0),
        "secondary": (255, 180, 0),
        "accent": (255,255,255),
        "overlay": 130,
        "style": "fire",
        "text": "white"
    },

    "conference": {
        "primary": (0, 70, 140),
        "secondary": (255,255,255),
        "accent": (0,200,255),
        "overlay": 100,
        "style": "professional",
        "text": "white"
    },

    "youth": {
        "primary": (0,150,100),
        "secondary": (255,215,0),
        "accent": (255,255,255),
        "overlay": 110,
        "style": "modern",
        "text": "white"
    },

    "fasting": {
        "primary": (45,0,90),
        "secondary": (255,215,0),
        "accent": (255,255,255),
        "overlay": 140,
        "style": "deep prayer",
        "text": "white"
    },

    "default": {
        "primary": (20,20,20),
        "secondary": (255,215,0),
        "accent": (255,255,255),
        "overlay": 100,
        "style": "classic",
        "text": "white"
    }

}
