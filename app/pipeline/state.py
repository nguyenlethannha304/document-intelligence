from typing import Any, TypedDict

from langchain_core.documents import Document


class PipelineState(TypedDict, total=False):
    document_id: str
    source_path: str
    ocr_engine: str
    document_type: str
    pages: list[Document]
    metadata: dict[str, Any]
    text: str
    output_path: str
    status: str
    error: str
