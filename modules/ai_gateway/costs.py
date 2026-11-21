"""
InChristAlone AI Cost Engine v4.11.8

Defines AI service unit costs.

Keeps pricing separate from:
- Gateway logic
- Billing logic
- AI providers
"""

AI_TASK_COSTS = {
    "general": 1,

    # Ministry Content
    "prayer_guide": 2,
    "bible_study": 3,
    "sermon_outline": 5,
    "theological_research": 5,

    # Church Operations
    "church_policy": 5,
    "event_planning": 3,

    # Creative Tools
    "flyer_generation": 10,
    "quiz_generation": 3,
    "website_content": 3,
}


def get_task_cost(task=None):
    """
    Return AI unit cost based on task.

    Unknown tasks default to general cost.
    """

    if not task:
        return AI_TASK_COSTS["general"]

    return AI_TASK_COSTS.get(
        task,
        AI_TASK_COSTS["general"]
    )
