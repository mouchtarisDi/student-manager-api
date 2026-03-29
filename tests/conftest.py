"""
Pytest shared configuration and fixtures.

This module defines reusable fixtures for tests, including:
- a dedicated test database
- database dependency overrides for FastAPI
- a test client for making API requests

Why this file matters:
- centralizes shared test setup
- avoids repeating setup code in every test
- keeps tests isolated from the real application database
"""

import os

# IMPORTANT:
# Set test environment BEFORE importing the app/settings modules.
os.environ["APP_ENV"] = "test"
os.environ["DATABASE_URL"] = "sqlite:///./test_students.db"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.session import get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test_students.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    """
    Provide a test database session instead of the real application database.

    Yields:
        A SQLAlchemy session connected to the test database.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    """
    Create a fresh test client for each test function.

    Before each test:
    - create all tables in the test database
    - override FastAPI's get_db dependency

    After each test:
    - clear dependency overrides
    - drop all tables
    - dispose the SQLAlchemy engine
    - delete the SQLite test database file

    Yields:
        A FastAPI TestClient instance.
    """
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

    if os.path.exists("test_students.db"):
        os.remove("test_students.db")
