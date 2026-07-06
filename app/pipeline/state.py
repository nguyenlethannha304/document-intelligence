from typing import Any, TypedDict

from langchain_core.documents import Document


class PipelineState(TypedDict, total=False):
    document_id: str
    source_path: str
    document_type: str
    ocr_engine: str
    pages: list[Document]
    metadata: dict[str, Any]
    text: setattr
    output_path: str
    status: str
    error: str
    ocr_needed: bool