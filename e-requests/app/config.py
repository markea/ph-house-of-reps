import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "HRep e-Request Portal"
    APP_ENV: str = os.getenv("APP_ENV", "local")  # Defaults to "local"
    PORT: int = int(os.getenv("PORT", "8080"))
    
    # Database
    # Local defaults to sqlite for 1-command startup, or postgres via DATABASE_URL
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./erequests_local.db"
    )
    
    # Storage
    STORAGE_TYPE: str = os.getenv("STORAGE_TYPE", "local")  # 'local' or 'gcs'
    LOCAL_UPLOAD_DIR: str = os.getenv("LOCAL_UPLOAD_DIR", "./uploads")
    GCS_BUCKET_NAME: str = os.getenv("GCS_BUCKET_NAME", "hrep-erequests-prod-storage")
    
    # Auth
    AUTH_MODE: str = os.getenv("AUTH_MODE", "mock")  # 'mock' or 'iap'
    
    # Gemini / ADK Agent
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Ensure local upload directory exists if in local mode
if settings.STORAGE_TYPE == "local":
    os.makedirs(settings.LOCAL_UPLOAD_DIR, exist_ok=True)
