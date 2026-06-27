from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "CarScanner"
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    R2_ACCOUNT_ID: str
    R2_ACCESS_KEY: str
    R2_SECRET_KEY: str
    R2_BUCKET: str
    R2_PUBLIC_URL: str

    INFERENCE_SERVICE_URL: str  # Vast.ai endpoint
    SUPABASE_URL: str
    SUPABASE_KEY: str

    ALLOWED_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()