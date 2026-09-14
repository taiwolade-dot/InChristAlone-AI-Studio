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


def get_memory_statistics(user_id=None):

    query = MinistryMemory.query

    if user_id:
        query = query.filter_by(
            user_id=user_id
        )

    total = query.count()

    high_priority = query.filter_by(
        importance="High"
    ).count()

    categories = {}

    memories = query.all()

    for memory in memories:
        categories[memory.memory_type] = (
            categories.get(memory.memory_type, 0) + 1
        )

    return {
        "total_memories": total,
        "high_priority": high_priority,
        "categories": categories,
        "recent_count": min(total, 5)
    }


def intelligent_memory_search(
    keyword,
    memory_type=None,
    importance=None,
    user_id=None
):

    query = MinistryMemory.query.filter(
        MinistryMemory.content.contains(keyword)
        |
        MinistryMemory.title.contains(keyword)
    )

    if user_id:
        query = query.filter_by(
            user_id=user_id
        )

    if memory_type:
        query = query.filter_by(
            memory_type=memory_type
        )

    if importance:
        query = query.filter_by(
            importance=importance
        )

    memories = query.order_by(
        MinistryMemory.created_at.desc()
    ).all()

    return [
        {
            "title": item.title,
            "type": item.memory_type,
            "importance": item.importance,
            "content": item.content,
            "source": item.source
        }
        for item in memories
    ]


def get_memory_timeline(user_id=None, limit=10):

    query = MinistryMemory.query

    if user_id:
        query = query.filter_by(
            user_id=user_id
        )

    memories = (
        query
        .order_by(
            MinistryMemory.created_at.desc()
        )
        .limit(limit)
        .all()
    )

    return [
        {
            "date": item.created_at.strftime("%Y-%m-%d")
                if item.created_at else "Unknown",
            "title": item.title,
            "type": item.memory_type,
            "importance": item.importance,
            "source": item.source
        }
        for item in memories
    ]


def get_memory_timeline(user_id=None, limit=10):

    query = MinistryMemory.query

    if user_id:
        query = query.filter_by(
            user_id=user_id
        )

    memories = (
        query
        .order_by(
            MinistryMemory.created_at.desc()
        )
        .limit(limit)
        .all()
    )

    return [
        {
            "date": item.created_at.strftime("%Y-%m-%d")
                if item.created_at else "Unknown",
            "title": item.title,
            "type": item.memory_type,
            "importance": item.importance,
            "source": item.source
        }
        for item in memories
    ]
