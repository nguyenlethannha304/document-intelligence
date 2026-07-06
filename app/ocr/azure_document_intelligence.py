from langchain_core.documents import Document

from app.ocr.base import BaseOCREngine


class AzureDocumentIntelligenceEngine(BaseOCREngine):
    name = "azure_document_intelligence"

    def extract_text(self, pages: list[Document]) -> str:
        return "\n\n".join(page.page_content for page in pages)
