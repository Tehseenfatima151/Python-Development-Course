"""
Application Configuration

Defines configuration classes for different environments (development,
testing, production). All sensitive values are sourced from environment
variables — never hard-coded.
"""

import os


class BaseConfig:
    """Shared configuration values across all environments."""

    # Secret key for session signing and CSRF protection.
    # Must be overridden in production via the SECRET_KEY environment variable.
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-value")

    # Disable debug mode by default; overridden in DevelopmentConfig.
    DEBUG: bool = False

    # Disable testing mode by default; overridden in TestingConfig.
    TESTING: bool = False

    # The name shown in API responses.
    APP_NAME: str = os.getenv("APP_NAME", "Dockerized Flask CI/CD App")

    # Active environment label surfaced through the root endpoint.
    FLASK_ENV: str = os.getenv("FLASK_ENV", "production")


class DevelopmentConfig(BaseConfig):
    """Configuration for local development."""

    DEBUG: bool = True
    FLASK_ENV: str = "development"


class TestingConfig(BaseConfig):
    """Configuration used during automated tests."""

    TESTING: bool = True
    DEBUG: bool = True
    FLASK_ENV: str = "testing"

    # Use a fixed, safe secret key during tests.
    SECRET_KEY: str = "test-secret-key"


class ProductionConfig(BaseConfig):
    """Configuration for production deployments."""

    DEBUG: bool = False
    FLASK_ENV: str = "production"


# Maps environment name strings to their corresponding config class.
_CONFIG_MAP: dict[str, type[BaseConfig]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(config_name: str | None = None) -> BaseConfig:
    """
    Return the appropriate configuration object.

    Resolution order:
    1. Explicit ``config_name`` argument.
    2. The ``FLASK_ENV`` environment variable.
    3. Falls back to 'development'.

    Args:
        config_name: Override the environment name.

    Returns:
        An instantiated configuration object.
    """
    env = config_name or os.getenv("FLASK_ENV", "development")
    config_class = _CONFIG_MAP.get(env, DevelopmentConfig)
    return config_class()
