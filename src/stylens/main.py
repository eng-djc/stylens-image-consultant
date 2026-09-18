"""StyLens FastAPI application factory."""

from fastapi import FastAPI

from stylens import __version__
from stylens.api.routes import router
from stylens.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="Human-centered decision support for professional image consultants.",
    )
    app.include_router(router, prefix=settings.api_prefix)
    return app


app = create_app()

