"""
InChristAlone AI Usage Tracker v4.11.4

Records AI consumption events.

Connects:
AI Gateway
    |
    ▼
AIUsageLog
    |
    ▼
Future Wallet Unit System
"""

from models import db, AIUsageLog


def log_ai_usage(
    user_id,
    provider=None,
    model=None,
    task=None,
    units_used=0,
    status="success",
    church_id=None
):
    """
    Record AI usage activity.
    """

    usage = AIUsageLog(
        user_id=user_id,
        church_id=church_id,
        provider=provider,
        model=model,
        task=task,
        units_used=units_used,
        status=status
    )

    db.session.add(usage)
    db.session.commit()

    return usage
