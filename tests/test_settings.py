from structured_freedom.config.settings import Settings


def test_settings_support_explicit_values() -> None:
    settings = Settings(
        APP_ENV="test",
        LOG_LEVEL="DEBUG",
        DATABASE_URL="sqlite+pysqlite:///:memory:",
        AI_PROVIDER="ollama",
        AI_DEFAULT_MODEL="llama3.1:8b",
        OLLAMA_BASE_URL="http://localhost:11434",
    )

    assert settings.app_env == "test"
    assert settings.log_level == "DEBUG"
    assert settings.ai_provider == "ollama"
