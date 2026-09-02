import io
import pytest
from app.services.storage import LocalStorageService
from fastapi import UploadFile, HTTPException

@pytest.mark.asyncio
async def test_local_storage_upload(tmp_path):
    storage = LocalStorageService(base_dir=str(tmp_path))
    fake_content = b"Sample PDF document for test"
    file = UploadFile(filename="affidavit.pdf", file=io.BytesIO(fake_content))

    path, url = await storage.upload_file(file, subfolder="tests")
    assert path.endswith(".pdf")
    assert "/uploads/" in url

@pytest.mark.asyncio
async def test_disallowed_extension(tmp_path):
    storage = LocalStorageService(base_dir=str(tmp_path))
    fake_content = b"malicious executable"
    file = UploadFile(filename="script.exe", file=io.BytesIO(fake_content))

    with pytest.raises(HTTPException) as excinfo:
        await storage.upload_file(file, subfolder="tests")
    assert excinfo.value.status_code == 400
