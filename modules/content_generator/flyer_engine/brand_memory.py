from models import ChurchBrandProfile


DEFAULT_BRAND_PROFILE = {
    "primary_color": "#1a2a6c",
    "accent_color": "#d4af37",
    "style": "premium Christian ministry",
    "tone": "inspiring",
    "layout": "modern"
}


def get_brand_profile(church_id=None):

    """
    Retrieve church AI branding identity from database.

    Falls back to default Christian ministry branding
    when no church profile exists.
    """

    if church_id:

        brand = ChurchBrandProfile.query.filter_by(
            church_id=church_id
        ).first()

        if brand:
            return {
                "primary_color": brand.primary_color,
                "accent_color": brand.accent_color,
                "style": brand.visual_style,
                "tone": brand.ministry_tone,
                "layout": brand.preferred_layout,
                "logo_position": brand.logo_position
            }

    return DEFAULT_BRAND_PROFILE
