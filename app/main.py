"""
Main application entry point.

This module creates the FastAPI application instance and registers the available routes.

It is the file that Uvicorn imports to run the server.
"""
from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.core.config import settings


app = FastAPI(
    title = settings.app_name, #δυναμικη αναθεση απο config
    debug = settings.app_debug, #$δυναμικη αναθεση απο config
)

app.include_router(health_router) #συνδεση των routes υγειας με την εφαρμογη