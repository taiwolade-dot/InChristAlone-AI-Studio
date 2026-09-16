def detect_occasion_type(title):
    """
    Detect the likely ministry occasion category.
    """

    text = title.lower()

    if "birthday" in text:
        return "Birthday"

    if "anniversary" in text:
        return "Anniversary"

    if "conference" in text:
        return "Conference"

    if "revival" in text:
        return "Revival"

    if "thanksgiving" in text:
        return "Thanksgiving"

    return "General"


def get_ai_actions(occasion_type):
    """
    Return available AI ministry actions.
    """

    actions = {
        "Birthday": [
            "Generate Flyer",
            "Generate Prayer",
            "Generate Greeting"
        ],

        "Anniversary": [
            "Generate Flyer",
            "Generate Prayer",
            "Generate Appreciation Message"
        ],

        "Conference": [
            "Generate Flyer",
            "Generate Prayer",
            "Generate Announcement",
            "Generate Bible Study Outline",
            "Generate Programme Outline"
        ],

        "Revival": [
            "Generate Flyer",
            "Generate Prayer",
            "Generate Scripture Reflection"
        ],

        "Thanksgiving": [
            "Generate Flyer",
            "Generate Prayer",
            "Generate Testimony Theme"
        ]
    }

    return actions.get(
        occasion_type,
        [
            "Generate Flyer",
            "Generate Prayer",
            "Generate Announcement"
        ]
    )


def build_occasion_context(occasion):
    """
    Prepare MinistryOccasion data for AI generation.
    """

    occasion_type = (
        occasion.occasion_type
        if occasion.occasion_type
        else detect_occasion_type(occasion.title)
    )

    return {
        "title": occasion.title,
        "occasion_type": occasion_type,
        "date": occasion.date,
        "scripture_theme": occasion.scripture_theme,
        "description": occasion.description,
        "ai_actions": get_ai_actions(occasion_type)
    }
