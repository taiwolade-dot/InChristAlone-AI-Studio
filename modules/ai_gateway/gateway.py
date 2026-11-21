"""
InChristAlone AI Gateway v4.11

Central AI access layer.

Features:
- Unified AI entry point
- AI Router integration
- Future support for Gemini, Claude, OpenAI
- Task-aware routing
- Usage tracking
"""

from modules.ai_gateway.router import route


def run_ai(prompt, task=None, context=None):
    """
    Unified AI gateway entry point.

    Parameters:
        prompt: User request
        task: Optional task type
        context: Optional ministry/church context

    Returns:
        AI response
    """
    return route(
        prompt=prompt,
        task=task,
        context=context,
    )
