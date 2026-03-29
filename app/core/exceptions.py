"""
Application-level custom exceptions.

This module contains domain and application exceptions that are raised
from the service layer and translated into HTTP responses by the API layer.

Why this module exists:
- keeps FastAPI-specificexceptions out of the service layer
- makes business logic easier to test
- improves separation of concerns between layers
"""


class AppError(Exception):
    """Base application exception.

    This can be used as a common parent for custom application errors."""


class NotFoundError(AppError):
    """
    Raised when a requested resource dos not exist."""


class ConflictError(AppError):
    """Raised when an operation conflicts with existing data."""
