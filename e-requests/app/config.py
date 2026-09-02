import os
import logging
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "HRep e-Request Portal"
    APP_ENV: str = os.getenv("APP_ENV", "local")  # 'local' or 'production'
    PORT: int = int(os.getenv("PORT", "8080"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./erequests_local.db"
    )
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "10"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))
    DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "1800"))
    
    # Storage Configuration
    STORAGE_TYPE: str = os.getenv("STORAGE_TYPE", "local")  # 'local' or 'gcs'
    LOCAL_UPLOAD_DIR: str = os.getenv("LOCAL_UPLOAD_DIR", "./uploads")
    GCS_BUCKET_NAME: str = os.getenv("GCS_BUCKET_NAME", "hrep-erequests-prod-storage")
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "25"))
    
    # Security & IAP Configuration
    AUTH_MODE: str = os.getenv("AUTH_MODE", "mock")  # 'mock' or 'iap'
    IAP_AUDIENCE: str = os.getenv("IAP_AUDIENCE", "") # e.g., /projects/PROJECT_NUMBER/global/backendServices/SERVICE_ID
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "*")
    
    # AI / Gemini API Key (Optional for local testing)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    def get_cors_origins(self) -> List[str]:
        if self.ALLOWED_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("erequests")

# Ensure local upload directory exists if in local mode
if settings.STORAGE_TYPE == "local":
    os.makedirs(settings.LOCAL_UPLOAD_DIR, exist_ok=True)
