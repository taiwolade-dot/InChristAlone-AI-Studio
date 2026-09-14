from models import MinistryMemory, db
from datetime import datetime


def save_ministry_memory(
    title,
    content,
    memory_type="Insight",
    source="AI Ministry Copilot",
    importance="Medium",
    user_id=None
):
    memory = MinistryMemory(
        user_id=user_id,
        memory_type=memory_type,
        title=title,
        content=content,
        source=source,
        importance=importance
    )

    db.session.add(memory)
    db.session.commit()

    return memory


def retrieve_ministry_memory(user_id=None, limit=10):

    query = MinistryMemory.query

    if user_id:
        query = query.filter_by(
            user_id=user_id
        )

    return (
        query
        .order_by(
            MinistryMemory.created_at.desc()
        )
        .limit(limit)
        .all()
    )


def search_ministry_memory(keyword, user_id=None):

    query = MinistryMemory.query.filter(
        MinistryMemory.content.contains(keyword)
        |
        MinistryMemory.title.contains(keyword)
    )

    if user_id:
        query = query.filter_by(
            user_id=user_id
        )

    return query.all()


def summarize_ministry_memory(user_id=None):

    memories = retrieve_ministry_memory(
        user_id=user_id,
        limit=5
    )

    return [
        {
            "title": item.title,
            "type": item.memory_type,
            "importance": item.importance,
            "content": item.content
        }
        for item in memories
    ]
