"""
InChristAlone AI Router v4.11

Selects the appropriate AI provider.

Future versions will support:
- Task-aware routing
- Cost-aware routing
- Automatic failover
- Tenant preferences
"""

from config import Config
from modules.ai_gateway.providers import (
    gemini_provider,
    claude_provider,
    openai_provider,
)


def route(prompt, task=None, context=None):
    provider = getattr(Config, "AI_DEFAULT_PROVIDER", "gemini").lower()

    if provider == "claude":
        return claude_provider(prompt)

    if provider == "openai":
        return openai_provider(prompt)

    return gemini_provider(prompt)
