from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    content_type: str | None = None
    storage_path: str
    status: str = "uploaded"
    ocr_needed: bool = False
