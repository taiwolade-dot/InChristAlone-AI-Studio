from models import AIConversation
from sqlalchemy import func

from .ministry_copilot import generate_ministry_copilot_context
from .memory_engine import get_memory_statistics, get_memory_timeline
from .knowledge_graph import build_memory_graph


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

    memory_stats = get_memory_statistics(user_id)

    memory_timeline = get_memory_timeline(user_id)

    memory_graph = build_memory_graph(user_id)


    return {
        "total": total,
        "recent": recent,
        "usage": usage,
        "copilot": copilot,
        "memory_stats": memory_stats,
        "memory_timeline": memory_timeline,
        "memory_graph": memory_graph
    }
