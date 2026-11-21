"""
InChristAlone AI Gateway v4.11

Central AI access layer.
Future support:
- Gemini
- Claude
- OpenAI
- Model routing
- Usage tracking
"""

from modules.ai_service import ask_ai


def run_ai(prompt, task=None, context=None):
    """
    Unified AI gateway entry point.

    Parameters:
        prompt: User request
        task: Future routing category
        context: Future church/ministry context

    Returns:
        AI response
    """

    return ask_ai(prompt)
