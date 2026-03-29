"""
Health check routes.

These endpoints are commonly used by monitoring systems, container platforms,
load balancers, and developers to confirm that the application is running.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health_check():
    """
    Basic health check endpoint.

    Returns a simple response indicating that the API process is up and able
    to respond requests.

    Returns:
    A dictionary with a basic application status."""
    return {"status": "ok"}


@router.get("/details")
def health_details():
    """
    Detailed health information endpoint.

    Returns bassic metadata about the application environment.
    This is helpful during development and debugging.

    Returns:
    A dictionary with application metadata and environment info."""

    return {
        "status": "ok",
        "service": "Student-center-api",
    }
