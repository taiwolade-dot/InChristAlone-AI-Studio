"""
InChristAlone AI Service Catalog v4.11.9

Provides a central list of available AI ministry services.

Used for:
- API discovery
- Future marketplace UI
- Service selection
"""

AI_SERVICE_CATALOG = {
    "general": {
        "name": "General AI Assistant",
        "description": "General ministry assistance and conversation",
        "units": 1,
    },

    "prayer_guide": {
        "name": "Prayer Guide Generator",
        "description": "Creates prayer guides and devotion resources",
        "units": 2,
    },

    "bible_study": {
        "name": "Bible Study Builder",
        "description": "Creates Bible study outlines and discipleship materials",
        "units": 3,
    },

    "sermon_outline": {
        "name": "Sermon Preparation Assistant",
        "description": "Creates sermon outlines, illustrations, and applications",
        "units": 5,
    },

    "theological_research": {
        "name": "Theological Research Assistant",
        "description": "Supports biblical and theological research",
        "units": 5,
    },

    "event_planning": {
        "name": "Church Event Planner",
        "description": "Assists with ministry event planning",
        "units": 3,
    },

    "flyer_generation": {
        "name": "AI Flyer Creator",
        "description": "Generates ministry flyers and creative materials",
        "units": 10,
    },

    "quiz_generation": {
        "name": "Bible Quiz Generator",
        "description": "Creates Bible quizzes and competitions",
        "units": 3,
    },

    "website_content": {
        "name": "Website Content Assistant",
        "description": "Creates church website content",
        "units": 3,
    },
}


def get_service_catalog():
    """
    Return all available AI services.
    """

    return AI_SERVICE_CATALOG


def get_service(service_key):
    """
    Return a single AI service.
    """

    return AI_SERVICE_CATALOG.get(service_key)
