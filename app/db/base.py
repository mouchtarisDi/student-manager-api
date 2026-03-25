# συγκεντρωνει ολα τα models σε ενα σημειο για ευκολη προσβαση
"""
Database model registry.

This module imports all SQLAlchemy models so that they are registered
with the application's declarative Base metadata

Why this file is usefull:
- it provides a single place to import all ORM models
- it ensures models are known before the table creation runs
- it becomes especially important later eith Alembic migrations
"""

from app.db.session import Base
from app.models.student import Student

__all__ = ["Base", "Student"]