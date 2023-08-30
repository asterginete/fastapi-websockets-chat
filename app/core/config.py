import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Chat App"
    APP_VERSION: str = "1.0"
    DEBUG: bool = True

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    DATABASE_MAX_CONNECTIONS: int = int(os.getenv("DATABASE_MAX_CONNECTIONS", 10))
    DATABASE_MIN_CONNECTIONS: int = int(os.getenv("DATABASE_MIN_CONNECTIONS", 2))

    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret_key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    ALGORITHM: str = "HS256"

    # Other potential configurations can be added here

    class Config:
        env_file = ".env"  # Load environment variables from .env file

settings = Settings()
