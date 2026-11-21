"""
InChristAlone AI Gateway v4.11.6

Central AI access layer.

Features:
- Unified AI entry point
- AI Router integration
- AI billing enforcement
- AI usage tracking
"""

from modules.ai_gateway.router import route
from modules.ai_gateway.usage import log_ai_usage
from modules.ai_gateway.billing import check_ai_units, deduct_ai_units


AI_REQUEST_COST = 1


def run_ai(prompt, task=None, context=None, user_id=1, church_id=None):
    """
    Unified AI gateway entry point.
    """

    if not check_ai_units(user_id, AI_REQUEST_COST):
        return (
            "Insufficient AI units. "
            "Please recharge your account to continue."
        )

    response = route(
        prompt=prompt,
        task=task,
        context=context,
    )

    deduct_ai_units(
        user_id=user_id,
        units=AI_REQUEST_COST
    )

    log_ai_usage(
        user_id=user_id,
        provider="gateway",
        model="auto",
        task=task or "general",
        units_used=AI_REQUEST_COST,
        status="success",
        church_id=church_id,
    )

    return response
