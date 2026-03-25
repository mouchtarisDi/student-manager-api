"""
Application configuration settings.

This module is responsible for loading the application's settings from environment
variable. It centralizes configuration in one place, so the rest of the codebase
does not need to read environment variables directly.

Why thiw is useful:
-avoids hardcoded values
-makes the app easier to configure perenvironment
-keeps secrets and environment-specific values outside the source code
"""
# Διαβαζει τιμες απο env variables και τις πετατρεπει σε σωστους Python τυπους.
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Aplication settings loaded from environment variables.
    
    Each attribure is automatically populated from the '.env' file or from real environment
    variables in the operating system / container.

    Attributes:
    app_name: The display name of the application.
    app_env: The current environment (e.g., development, production).
    app_debug: Whether to enable debug mode (True/False).
    database_url: The connection URL for the database.
    """

    app_name: str = "Student Center Api"
    app_env: str = "development"
    app_debug: bool = True
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

# Δημιουργουμε ενα ετοιμο object για να το εισαγουμε οπου χρειαστει.
settings = Settings()