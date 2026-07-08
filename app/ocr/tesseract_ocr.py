import requests

from langchain_core.documents import Document
from app.ocr.base import BaseOCREngine

class TesseractOCREngine(BaseOCREngine):
    name = "tesseract"
    def extract_text(self, page: Document) -> Document:
        print(f"Running Tesseract OCR on page {page.page_number}...")
        content = page.page_content
        # Here you would implement the actual Tesseract OCR logic.
        response = requests.post("http://ocr-service:8080/ocr", data={"content": content})
        if response.status_code == 200:
        return page