from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain_core.documents import Document
from openai import OpenAI

from app.core.config import get_settings
from app.ocr.base import BaseOCREngine


class LLMOCREngine(BaseOCREngine):
    name = "llm_ocr"

    def __init__(self):
        if get_settings().production:
            self.client = OpenAI(
                base_url=get_settings().azure_project_endpoint,
                api_key=get_settings().openai_api_key,
            )
        else:
            self.client = None

    def _ai_ocr(self, page: Document) -> Document:
        model = (
            get_settings().llm_model
            if page.metadata.get("avg_confidence", 0) < 60
            else get_settings().slm_model
        )
        image_url = page.metadata.get("image_url")
        response = self.client.responses.create(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": "You are an OCR engine that extracts text from images.",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Extract text from this image only.",
                        },
                        {
                            "type": "input_image",
                            "image_url": image_url,
                        },
                    ],
                },
            ],
        )
        print(response)
        return response.output_text if response.output_text else "No text extracted."

    def extract_text(self, page: Document) -> Document:
        page_index = page.metadata.get("page", "unknown")
        avg_confidence = page.metadata.get("avg_confidence", 0)
        print(f"Running AI LLM OCR on page {page_index}...")
        if self.client:
            print(f"Actual running LLM OCR on page {page_index}...")
            page.page_content = self._ai_ocr(page)
            page.metadata["ocr_needed"] = False
        return page
