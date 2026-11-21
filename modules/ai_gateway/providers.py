"""
InChristAlone AI Gateway Providers v4.11

Provider abstraction layer.

Supported providers:
- Gemini (current)
- Claude (planned)
- OpenAI (planned)
"""

from modules.ai_service import ask_ai


def gemini_provider(prompt):
    """
    Gemini AI provider.
    Current production provider.
    """
    return ask_ai(prompt)


def claude_provider(prompt):
    """
    Claude provider placeholder.
    """
    return (
        "Claude provider is not yet connected."
    )


def openai_provider(prompt):
    """
    OpenAI provider placeholder.
    """
    return (
        "OpenAI provider is not yet connected."
    )
