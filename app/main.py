"""
Main application entry point.

This module creates the FastAPI application instance,
registers all routes, and initializes database tables.

Important note:
For now we use Base.metadata.create_all() to create tables automatically.
Later, when we introduce Alembic, migrations will take over this job.
"""

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.students import router as student_router
from app.core.config import settings
from app.db import base  # noqa: F401
from app.db.session import Base, engine

app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
)

Base.metadata.create_all(bind=engine)

app.include_router(health_router)
app.include_router(student_router)