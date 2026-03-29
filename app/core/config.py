"""
Application configuration module.

This module loads the application's settings from environment variables.

Why this is useful:
- avoids hardcoded values
- centralizes configuration
- makes different environments easier to support
  (development, test, production, etc.)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        app_name: Human-readable application name.
        app_env: Current environment (development, test, production).
        app_debug: Whether debug mode is enabled.
        database_url: Database connection string.
    """

    app_name: str = "Student Center API"
    app_env: str = "development"
    app_debug: bool = True
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def is_test(self) -> bool:
        """
        Return True when the application is running in test mode.

        This helps us disable production-style startup behavior during tests.
        """
        return self.app_env.lower() == "test"


settings = Settings()
