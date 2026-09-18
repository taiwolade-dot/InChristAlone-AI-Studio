CHURCH_BRAND_MEMORY = {

    "default": {
        "primary_color": "#1a2a6c",
        "accent_color": "#d4af37",
        "style": "premium Christian ministry",
        "tone": "inspiring",
        "layout": "modern"
    }

}


def get_brand_profile(
    church_name="default"
):

    return CHURCH_BRAND_MEMORY.get(
        church_name,
        CHURCH_BRAND_MEMORY["default"]
    )
