"""
InChristAlone AI Gateway v4.11.7

Central AI access layer.

Features:
- Unified AI entry point
- AI Router integration
- Transaction-safe billing
- AI usage tracking
"""

from modules.ai_gateway.router import route
from modules.ai_gateway.usage import log_ai_usage
from modules.ai_gateway.transactions import (
    charge_ai_request,
    refund_ai_request,
)


AI_REQUEST_COST = 1


def run_ai(prompt, task=None, context=None, user_id=1, church_id=None):
    """
    Unified AI gateway entry point.
    """

    if not charge_ai_request(user_id, AI_REQUEST_COST):
        return (
            "Insufficient AI units. "
            "Please recharge your account to continue."
        )

    try:
        response = route(
            prompt=prompt,
            task=task,
            context=context,
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

    except Exception as error:
        refund_ai_request(
            user_id,
            AI_REQUEST_COST
        )

        return f"AI generation failed: {error}"
