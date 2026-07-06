from azure.core.credentials import DefaultAzureCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from langchain_core.documents import Document
from app.ocr.base import BaseOCREngine


class AzureDocumentIntelligenceEngine(BaseOCREngine):
    name = "azure_document_intelligence"
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        credential = DefaultAzureCredential()
        self.client = DocumentIntelligenceClient(endpoint, credential)
        self.ai_model = 
    def extract_text(self, pages: list[Document]) -> str:

        return "\n\n".join(page.page_content for page in pages)
