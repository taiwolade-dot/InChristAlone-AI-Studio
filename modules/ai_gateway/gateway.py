"""
InChristAlone AI Gateway v4.11.8

Central AI access layer.

Features:
- Unified AI entry point
- AI Router integration
- Transaction-safe billing
- Dynamic task costing
- AI usage tracking
"""

from modules.ai_gateway.router import route
from modules.ai_gateway.usage import log_ai_usage
from modules.ai_gateway.transactions import (
    charge_ai_request,
    refund_ai_request,
)
from modules.ai_gateway.costs import get_task_cost


def run_ai(prompt, task=None, context=None, user_id=1, church_id=None):
    """
    Unified AI gateway entry point.
    """

    request_cost = get_task_cost(task)

    if not charge_ai_request(user_id, request_cost):
        return (
            f"Insufficient AI units. "
            f"This request requires {request_cost} units."
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
            units_used=request_cost,
            status="success",
            church_id=church_id,
        )

        return response

    except Exception as error:
        refund_ai_request(
            user_id,
            request_cost
        )

        return f"AI generation failed: {error}"
