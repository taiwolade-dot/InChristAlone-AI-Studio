"""
InChristAlone AI Gateway Health Monitor v4.11

Tracks AI provider availability.

Future support:
- API health checks
- Latency tracking
- Quota monitoring
- Automatic failover
"""

from config import Config


def provider_status():
    """
    Return current provider availability.
    """

    return {
        "gemini": bool(
            getattr(Config, "GEMINI_API_KEY", None)
        ),
        "claude": bool(
            getattr(Config, "ANTHROPIC_API_KEY", None)
        ),
        "openai": bool(
            getattr(Config, "OPENAI_API_KEY", None)
        ),
    }


def is_available(provider):
    """
    Check if a provider is configured.
    """

    providers = provider_status()

    return providers.get(
        provider.lower(),
        False
    )
