from app.ocr.base import BaseOCREngine
from langchain_core.documents import Document

class LLMOCREngine(BaseOCREngine):
    name = "llm_ocr"

    def extract_text(self, page: Document) -> Document:
        page_index = page.metadata.get("page", "unknown")
        print(f"Running LLM OCR on page {page_index}...")
        return page