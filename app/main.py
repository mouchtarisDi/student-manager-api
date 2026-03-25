"""
Main application entry point.

This module creates the FastAPI application instance,
registers all routes, and initializes database tables.

Important note:
For now we use Base.metadata.create_all() to create tables automatically.
Later in the project, Alembic migrations will replace this behavior.
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

    Code before `yield` runs during application startup.
    Code after `yield` runs during application shutdown.

    During startup we:
    1. wait for the database to be ready
    2. create database tables for registered models

    This startup flow is safer in containerized environments because
    the database service may need a few seconds before it can accept
    connections.

    Args:
        app: The FastAPI application instance.

    Yields:
        None. Control is passed back to FastAPI after startup finishes.
    """
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