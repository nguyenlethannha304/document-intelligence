from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain_core.documents import Document
from openai import OpenAI

from app.core.config import get_settings
from app.ocr.base import BaseOCREngine


class LLMOCREngine(BaseOCREngine):
    name = "llm_ocr"

    def __init__(self):
        if get_settings().production:
            token_provider = get_bearer_token_provider(
                credential=DefaultAzureCredential(),
                scopes=["https://ai.azure.com/.default"],
            )
            self.client = OpenAI(
                endpoint=get_settings().azure_project_endpoint,
                credential=token_provider,
            )
        else:
            self.client = None

    def _ai_ocr(self, page: Document) -> Document:
        model = (
            get_settings().llm_model
            if page.metadata.get("avg_confidence", 0) < 60
            else get_settings().slm_model
        )
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an OCR engine that extracts text from images.",
                },
                {
                    "role": "user",
                    "content": f"Extract text from the following image: {page.metadata.get('image_url')}",
                },
            ],
        )
        extracted_text = response.choices[0].message.content
        page.page_content = extracted_text
        return page

    def extract_text(self, page: Document) -> Document:
        page_index = page.metadata.get("page", "unknown")
        avg_confidence = page.metadata.get("avg_confidence", 0)
        print(
            f"Running {get_settings().slm_model if avg_confidence > 60 else get_settings().llm_model} OCR on page {page_index}..."
        )
        if self.client:
            page = self._ai_ocr(page)
        return page
