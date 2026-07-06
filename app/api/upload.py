from fastapi import APIRouter, File, UploadFile

from app.models.document import DocumentUploadResponse
from app.storage.local import save_upload

router = APIRouter(tags=["upload"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)) -> DocumentUploadResponse:
    document_id, storage_path = await save_upload(file)
    return DocumentUploadResponse(
        document_id=document_id,
        filename=file.filename or storage_path.name,
        content_type=file.content_type,
        storage_path=str(storage_path),
    )
