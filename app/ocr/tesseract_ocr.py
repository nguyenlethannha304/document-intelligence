import requests

from langchain_core.documents import Document
from app.ocr.base import BaseOCREngine

class TesseractOCREngine(BaseOCREngine):
    name = "tesseract"

    def extract_text(self, page: Document) -> Document:
        page_index = page.metadata.get("page", "unknown")
        print(f"Running Tesseract OCR on page {page_index}...")

        image_bytes = page.metadata.get("image_bytes")
        if not image_bytes:
            return page

        response = requests.post(
            "http://ocrservice:8080/ocr",
            files={
                "file": (
                    page.metadata.get("filename", "page.png"),
                    image_bytes,
                    page.metadata.get("content_type", "image/png"),
                )
            },
            data={"lang": "eng", "config": "--oem 3 --psm 6"},
            timeout=60,
        )

        if response.status_code == 200:
            payload = response.json()
            print(f"OCR result for page {page_index}: {payload}")
            if payload.get("avg_confidence", 0) > 0.8:
                page.page_content = payload.get("text", "")
                page.metadata["ocr_needed"] = False
        else:
            print(f"Error during OCR: {response.status_code} - {response.text}")
        return page