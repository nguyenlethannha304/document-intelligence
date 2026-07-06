from abc import ABC, abstractmethod

from langchain_core.documents import Document

from app.core.exceptions import OCRPlatformError


class BaseOCREngine(ABC):
    name: str

    @abstractmethod
    def extract_text(self, pages: list[Document]) -> str:
        raise NotImplementedError


def get_ocr_engine(name: str) -> BaseOCREngine:
    from app.ocr.azure_document_intelligence import AzureDocumentIntelligenceEngine

    engines: dict[str, BaseOCREngine] = {
        "azure_document_intelligence": AzureDocumentIntelligenceEngine(),
    }
    try:
        return engines[name]
    except KeyError as exc:
        raise OCRPlatformError(f"Unsupported OCR engine: {name}") from exc
