from models import AIConversation
from sqlalchemy import func
from datetime import datetime, timedelta


def ministry_insights(user_id):

    conversations = AIConversation.query.filter_by(
        user_id=user_id
    )

    total = conversations.count()

    modules = (
        conversations.with_entities(
            AIConversation.module,
            func.count(AIConversation.id)
        )
        .group_by(
            AIConversation.module
        )
        .all()
    )


    usage = {}

    for module, count in modules:
        usage[module] = count


    most_used = None

    if usage:
        most_used = max(
            usage,
            key=usage.get
        )


    recommendations = []


    if usage.get("prayer",0) > 10:
        recommendations.append(
            "Develop a prayer devotion resource"
        )


    if usage.get("sermon",0) > 10:
        recommendations.append(
            "Create a sermon archive"
        )


    if usage.get("seminary",0) > 5:
        recommendations.append(
            "Develop theological study materials"
        )


    return {
        "total_requests": total,
        "usage": usage,
        "most_used": most_used,
        "recommendations": recommendations
    }



def generate_ministry_insights(user_id):

    return ministry_insights(user_id)

