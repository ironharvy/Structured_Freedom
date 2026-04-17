"""DSPy language model configuration from application settings."""

from __future__ import annotations

import dspy

from structured_freedom.config.settings import Settings, get_settings

_configured = False


def configure_lm(settings: Settings | None = None) -> dspy.LM:
    """Configure and return the DSPy language model from settings.

    Calling this more than once with the same settings is safe — DSPy
    re-registers the global LM on every call but the object is lightweight.
    """
    active = settings or get_settings()

    if active.ai_provider == "ollama":
        model_string = f"ollama_chat/{active.ai_default_model}"
        lm = dspy.LM(
            model=model_string,
            api_base=active.ollama_base_url,
            api_key="ollama",
        )
    elif active.ai_provider == "openai":
        lm = dspy.LM(
            model=f"openai/{active.ai_default_model}",
            api_key=active.openai_api_key,
        )
    elif active.ai_provider == "anthropic":
        lm = dspy.LM(
            model=f"anthropic/{active.ai_default_model}",
            api_key=active.anthropic_api_key,
        )
    else:
        raise ValueError(f"Unsupported AI provider: {active.ai_provider!r}")

    dspy.configure(lm=lm)
    return lm
