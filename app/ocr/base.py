from abc import ABC, abstractmethod
from functools import lru_cache

from langchain_core.documents import Document

from app.core.exceptions import OCRPlatformError


class BaseOCREngine(ABC):
    name: str

    @abstractmethod
    def extract_text(self, page: Document) -> Document:
        raise NotImplementedError


@lru_cache(maxsize=2)
def get_ocr_engine(name: str) -> BaseOCREngine:
    from app.ocr.llm_ocr import LLMOCREngine
    from app.ocr.tesseract_ocr import TesseractOCREngine

    engines: dict[str, BaseOCREngine] = {
        "tesseract": TesseractOCREngine(),
        "llm_ocr": LLMOCREngine(),
    }
    try:
        return engines[name]
    except KeyError as exc:
        raise OCRPlatformError(f"Unsupported OCR engine: {name}") from exc
