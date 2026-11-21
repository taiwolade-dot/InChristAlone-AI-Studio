"""
InChristAlone AI Router v4.11

Selects the appropriate AI provider.

Features:
- Provider selection
- Provider availability checking
- Basic fallback support

Future versions:
- Task-aware routing
- Cost-aware routing
- Latency-aware routing
- Tenant preferences
"""

from config import Config
from modules.ai_gateway.providers import (
    gemini_provider,
    claude_provider,
    openai_provider,
)

from modules.ai_gateway.health import is_available


def route(prompt, task=None, context=None):
    """
    Select provider and execute AI request.
    """

    provider = getattr(
        Config,
        "AI_DEFAULT_PROVIDER",
        "gemini"
    ).lower()

    if is_available(provider):

        if provider == "claude":
            return claude_provider(prompt)

        if provider == "openai":
            return openai_provider(prompt)

        return gemini_provider(prompt)

    # Fallback sequence

    fallback_order = [
        "gemini",
        "claude",
        "openai",
    ]

    for fallback in fallback_order:

        if is_available(fallback):

            if fallback == "gemini":
                return gemini_provider(prompt)

            if fallback == "claude":
                return claude_provider(prompt)

            if fallback == "openai":
                return openai_provider(prompt)

    return (
        "⚠️ No AI provider is currently available."
    )
