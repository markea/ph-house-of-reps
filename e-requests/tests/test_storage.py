import io
import pytest
from app.services.storage import LocalStorageService
from fastapi import UploadFile, HTTPException

@pytest.mark.asyncio
async def test_local_storage_upload(tmp_path):
    storage = LocalStorageService(base_dir=str(tmp_path))
    fake_content = b"%PDF-1.4 Sample valid PDF document header and payload"
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

@pytest.mark.asyncio
async def test_spoofed_file_magic_bytes_rejected(tmp_path):
    storage = LocalStorageService(base_dir=str(tmp_path))
    # Malicious script disguised with a .pdf extension
    fake_content = b"#!/bin/bash\necho 'hacked'"
    file = UploadFile(filename="trojan.pdf", file=io.BytesIO(fake_content))

    with pytest.raises(HTTPException) as excinfo:
        await storage.upload_file(file, subfolder="tests")
    assert excinfo.value.status_code == 400
    assert "magic byte" in str(excinfo.value.detail)

