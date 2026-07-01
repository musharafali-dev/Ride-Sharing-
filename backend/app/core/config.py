from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "RideSphere API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "729cfcbbe1c3f25e985b46e300bd7326df21a28a38bc1a3a" # Mock key
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days
    
    # Try local PostgreSQL by default, fallback to SQLite if needed
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/ridesphere"
    REDIS_URL: str = "redis://127.0.0.1:6380/0"
    
    COMMISSION_RATE: float = 0.15 # 15% platform fee

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
