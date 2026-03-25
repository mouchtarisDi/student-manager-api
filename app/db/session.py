# Υπευθυνο για: συνδεση με τη βαση, το SQLAlchemy engine, τα sessions και το base class των models

"""
Database session engine configuration

This module creates the SQLAlchemy engine, the session factory and the declarative base used by ORM models

Why this exists:
-keeps database setup in one place
-allows the rest of the app to reuse the same session logic
-separates infrastructure cade from business logic
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base() # ολα τα models θα κληρονομουν απο αυτο

def get_db():
    """
    Provide a database session for each request
    
    This function is used as a FastAPI dependency.
    A new database session is created when the requeststarts,
    yielded to the route handler, and then always closed at the end
    
    Why this patternis important:
    -it avoids leaving open database connections
    -it gives each request its own session
    -it integrates cleanly with FastAPI's dependency injection system
    
    Yields:
    A SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()