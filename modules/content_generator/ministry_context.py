from models import ChurchProfile
from modules.content_generator.flyer_engine.brand_memory import get_brand_profile


def get_ministry_context(church_id=None):

    context = {
        "church": {},
        "brand": {}
    }

    if church_id:

        church = ChurchProfile.query.filter_by(
            id=church_id
        ).first()

        if church:
            context["church"] = {
                "name": church.church_name,
                "motto": church.motto,
                "vision": church.vision,
                "mission": church.mission,
                "statement_of_faith": church.statement_of_faith,
                "denomination": church.denomination,
                "association": church.association,
                "conference": church.conference
            }

    context["brand"] = get_brand_profile(church_id)

    return context
