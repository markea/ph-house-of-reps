import os
import uuid
from abc import ABC, abstractmethod
from typing import Tuple
from fastapi import UploadFile, HTTPException
from app.config import settings, logger

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".png", ".jpg", ".jpeg", ".xlsx", ".zip"}

class StorageService(ABC):
    @abstractmethod
    async def upload_file(self, file: UploadFile, subfolder: str = "") -> Tuple[str, str]:
        """Uploads a file and returns (storage_path, public_or_signed_url)."""
        pass

    @abstractmethod
    def get_file_url(self, file_path: str) -> str:
        """Returns access URL for a stored file."""
        pass

class LocalStorageService(StorageService):
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    async def upload_file(self, file: UploadFile, subfolder: str = "") -> Tuple[str, str]:
        self._validate_file(file)
        
        target_dir = os.path.join(self.base_dir, subfolder)
        os.makedirs(target_dir, exist_ok=True)
        
        ext = os.path.splitext(file.filename)[1].lower()
        safe_name = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(target_dir, safe_name)
        
        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(status_code=400, detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB")
            
        with open(file_path, "wb") as f:
            f.write(content)
            
        relative_path = os.path.relpath(file_path, self.base_dir)
        return relative_path, f"/uploads/{relative_path}"

    def get_file_url(self, file_path: str) -> str:
        return f"/uploads/{file_path}"

    def _validate_file(self, file: UploadFile):
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"File extension '{ext}' is not permitted.")

class GCSStorageService(StorageService):
    def __init__(self, bucket_name: str):
        from google.cloud import storage
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    async def upload_file(self, file: UploadFile, subfolder: str = "") -> Tuple[str, str]:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"File extension '{ext}' is not permitted.")
            
        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(status_code=400, detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB")
            
        safe_name = f"{uuid.uuid4()}{ext}"
        blob_path = f"{subfolder}/{safe_name}".strip("/")
        
        blob = self.bucket.blob(blob_path)
        blob.upload_from_string(content, content_type=file.content_type)
        logger.info(f"Uploaded attachment to GCS: gs://{self.bucket_name}/{blob_path}")
        
        return blob_path, self.get_file_url(blob_path)

    def get_file_url(self, file_path: str) -> str:
        # In production, generate 1-hour signed URL
        try:
            from datetime import timedelta
            blob = self.bucket.blob(file_path)
            return blob.generate_signed_url(expiration=timedelta(hours=1))
        except Exception as e:
            logger.warning(f"Failed to generate signed URL: {e}")
            return f"https://storage.googleapis.com/{self.bucket_name}/{file_path}"

def get_storage_service() -> StorageService:
    if settings.STORAGE_TYPE == "gcs" and settings.APP_ENV == "production":
        return GCSStorageService(settings.GCS_BUCKET_NAME)
    return LocalStorageService(settings.LOCAL_UPLOAD_DIR)
