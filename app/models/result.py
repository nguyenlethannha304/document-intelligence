from pydantic import BaseModel, Field


class OCRResult(BaseModel):
    document_id: str
    source_path: str
    engine: str
    page_count: int = 0
    text: str = Field(default="")
    status: str = Field(default="completed")
