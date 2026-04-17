"""Entry point for the FastAPI development server."""

import uvicorn

from structured_freedom.app.api.app import app
from structured_freedom.config.settings import get_settings


def main() -> None:
    settings = get_settings()
    uvicorn.run(
        "structured_freedom.app.api.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.app_env == "development",
    )


if __name__ == "__main__":
    main()
