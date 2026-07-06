from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import get_settings


async def save_upload(file: UploadFile) -> tuple[str, Path]:
    settings = get_settings()
    suffix = Path(file.filename or "document.pdf").suffix or ".pdf"
    document_id = str(uuid4())
    target_path = settings.upload_dir / f"{document_id}{suffix}"
    content = await file.read()
    target_path.write_bytes(content)
    return document_id, target_path


def write_text_output(document_id: str, text: str) -> Path:
    settings = get_settings()
    target_path = settings.output_dir / f"{document_id}.md"
    target_path.write_text(text, encoding="utf-8")
    return target_path
