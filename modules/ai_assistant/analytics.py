from models import AIConversation, db
from sqlalchemy import func


def get_ai_statistics(user_id=None):

    query = AIConversation.query

    if user_id:
        query = query.filter_by(
            user_id=user_id
        )

    total = query.count()


    module_usage = (
        db.session.query(
            AIConversation.module,
            func.count(AIConversation.id)
        )
        .filter(
            AIConversation.user_id == user_id
        )
        .group_by(
            AIConversation.module
        )
        .all()
        if user_id else
        db.session.query(
            AIConversation.module,
            func.count(AIConversation.id)
        )
        .group_by(
            AIConversation.module
        )
        .all()
    )


    modules = {}

    for module, count in module_usage:
        modules[module] = count


    most_used = None

    if modules:
        most_used = max(
            modules,
            key=modules.get
        )


    return {
        "total": total,
        "modules": modules,
        "most_used": most_used
    }
