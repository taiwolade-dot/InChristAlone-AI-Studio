from models import MinistryMemory


def create_memory_relationship(memory_a, memory_b):
    """
    Create a relationship between two ministry memories.
    """

    return {
        "source": memory_a.title,
        "target": memory_b.title,
        "relationship": "related",
        "source_type": memory_a.memory_type,
        "target_type": memory_b.memory_type
    }


def find_related_memories(memory, limit=5):
    """
    Find memories related by shared keywords.
    """

    keywords = set(
        memory.content.lower().split()
        +
        memory.title.lower().split()
    )

    memories = (
        MinistryMemory.query
        .filter(
            MinistryMemory.id != memory.id
        )
        .limit(50)
        .all()
    )

    related = []

    for item in memories:

        text = (
            item.title +
            " " +
            item.content
        ).lower()

        score = sum(
            1
            for keyword in keywords
            if keyword in text
        )

        if score > 0:
            related.append(
                {
                    "memory": item,
                    "score": score
                }
            )

    related.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return [
        item["memory"]
        for item in related[:limit]
    ]



def remove_duplicate_relationships(graph):

    seen = set()
    unique = []

    for item in graph:

        pair = tuple(
            sorted(
                [
                    item["source"],
                    item["target"]
                ]
            )
        )

        if pair not in seen:
            seen.add(pair)
            unique.append(item)

    return unique


def build_memory_graph(user_id=None):

    query = MinistryMemory.query

    if user_id:
        query = query.filter_by(
            user_id=user_id
        )

    memories = query.all()

    graph = []

    for memory in memories:

        related = find_related_memories(
            memory
        )

        for item in related:

            graph.append(
                create_memory_relationship(
                    memory,
                    item
                )
            )

    return remove_duplicate_relationships(graph)
