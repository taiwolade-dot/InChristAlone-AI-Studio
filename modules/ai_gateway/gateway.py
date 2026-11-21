"""
InChristAlone AI Gateway v4.11.4

Central AI access layer.

Features:
- Unified AI entry point
- AI Router integration
- Provider abstraction
- AI usage tracking
"""

from modules.ai_gateway.router import route
from modules.ai_gateway.usage import log_ai_usage


def run_ai(prompt, task=None, context=None, user_id=1, church_id=None):
    """
    Unified AI gateway entry point.

    Parameters:
        prompt: User request
        task: Optional task type
        context: Optional ministry/church context
        user_id: User making the request
        church_id: Optional church context

    Returns:
        AI response
    """

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
        units_used=1,
        status="success",
        church_id=church_id,
    )

    return response
