from models import AIConversation
from sqlalchemy import func

from .ministry_copilot import generate_ministry_copilot_context


def get_ai_dashboard(user_id):

    total = AIConversation.query.filter_by(
        user_id=user_id
    ).count()


    recent = (
        AIConversation.query
        .filter_by(user_id=user_id)
        .order_by(
            AIConversation.created_at.desc()
        )
        .limit(5)
        .all()
    )


    modules = (
        AIConversation.query
        .filter_by(user_id=user_id)
        .with_entities(
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


    copilot = generate_ministry_copilot_context()


    return {
        "total": total,
        "recent": recent,
        "usage": usage,
        "copilot": copilot
    }
