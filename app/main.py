"""
Main application entry point.

This module creates the FastAPI application instance,
registers all routes, and initializes startup behavior.

Important note:
In development/production-like environments, the app waits for the DB
and creates tables on startup.

In test mode, this startup DB logic is skipped because tests provide
their own isolated database setup.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.students import router as student_router
from app.core.config import settings
from app.db import base  # noqa: F401
from app.db.session import Base, engine, wait_for_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.

    Startup logic:
    - In normal app environments, wait for the DB and create tables.
    - In test mode, skip this logic because tests manage their own DB setup.

    Args:
        app: The FastAPI application instance.

    Yields:
        Control back to FastAPI once startup completes.
    """
    if not settings.is_test:
        wait_for_db()
        Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(student_router)
