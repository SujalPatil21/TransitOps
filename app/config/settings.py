import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class ConfigurationError(Exception):
    """
    Exception raised when application configuration is invalid or missing.
    """
    pass

class Settings(BaseSettings):
    """
    Application Settings configuration class.
    Loads variables from the environment or a .env file.
    """
    model_config = SettingsConfigDict(
        env_file=os.path.join(str(BASE_DIR), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Project metadata
    PROJECT_NAME: str = "FastAPI Auth Starter"

    # Database Configuration
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/test"

    # JWT Authentication Parameters
    JWT_SECRET: str = "super-secret-jwt-key-change-me-in-production-12345!"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # SMTP Configuration (Defaulting to Gmail)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_EMAIL: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    # OTP Configuration
    OTP_EXPIRY: int = 300       # 5 minutes
    RESEND_DELAY: int = 45      # 45 seconds
    ENABLE_LOGIN_OTP: bool = False

# Singleton instance of settings to be reused across the application
settings = Settings()

