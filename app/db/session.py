# Υπευθυνο για: συνδεση με τη βαση, το SQLAlchemy engine, τα sessions και το base class των models
"""
Database session and engine configuration.

This module is responsible for:
- creating the SQLAlchemy engine
- creating database sessions
- providing the shared declarative Base for ORM models
- offering a helper to wait until the database becomes available

Why this module exists:
- centralizes all DB connection logic
- keeps DB infrastructure separate from business logic
- makes the rest of the application cleaner and easier to maintain
"""

import time

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    """
    Provide a database session for each request.

    This function is used as a FastAPI dependency.
    A new database session is created when the request starts,
    yielded to the route handler, and then always closed at the end.

    Why this pattern is important:
    - avoids leaked DB connections
    - gives each request an isolated session
    - integrates cleanly with FastAPI dependency injection

    Yields:
        A SQLAlchemy session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def wait_for_db(max_retries: int = 10, delay_seconds: int = 2) -> None:
    """
    Wait until the database is available.

    This is especially useful in Docker Compose environments where the app
    container may start before PostgreSQL is fully ready to accept
    connections.

    The function tries to open a connection and execute a very small query.
    If that fails, it waits a bit and tries again.

    Args:
        max_retries: Maximum number of connection attempts.
        delay_seconds: Seconds to wait between attempts.

    Raises:
        Exception: Re-raises the last database connection exception if all
            retry attempts fail.
    """
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print(f"Database connection successful on attempt {attempt}.")
            return
        except Exception as exc:
            last_error = exc
            print(
                f"Database not ready yet (attempt {attempt}/{max_retries}). "
                f"Retrying in {delay_seconds} seconds..."
            )
            time.sleep(delay_seconds)

    raise last_error
