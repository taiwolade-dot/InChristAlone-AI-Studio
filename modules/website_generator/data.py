SITE_TYPES = {
    "church_website": {
        "label": "Church Website",
        "fields": [
            "church_name",
            "tagline",
            "address",
            "service_times",
            "phone",
            "email",
            "about_text",
            "pastor_name",
        ],
        "sections": ["hero", "about", "service_times", "contact", "footer"],
    },
    "ministry_landing": {
        "label": "Ministry Landing Page",
        "fields": [
            "ministry_name",
            "tagline",
            "mission_statement",
            "cta_text",
            "cta_link",
            "contact_email",
        ],
        "sections": ["hero", "mission", "cta", "footer"],
    },
}

COLOR_SCHEMES = {
    "royal_blue_gold": {
        "label": "Royal Blue & Gold (Default)",
        "primary": "#1a2a6c",
        "primary_dark": "#10193f",
        "accent": "#d4af37",
        "text": "#333333",
        "background": "#f5f5f7",
    },
    "deep_purple_white": {
        "label": "Deep Purple & White",
        "primary": "#4c1d95",
        "primary_dark": "#2e1065",
        "accent": "#ffffff",
        "text": "#2d2d2d",
        "background": "#faf5ff",
    },
    "forest_green_cream": {
        "label": "Forest Green & Cream",
        "primary": "#166534",
        "primary_dark": "#0f3d20",
        "accent": "#f5deb3",
        "text": "#2d2d2d",
        "background": "#fdfaf5",
    },
}