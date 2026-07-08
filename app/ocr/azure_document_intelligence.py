from azure.core.credentials import DefaultAzureCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from langchain_core.documents import Document
from app.ocr.base import BaseOCREngine


class AzureDocumentIntelligenceEngine(BaseOCREngine):
    name = "azure_document_intelligence"
    def __init__(self):
        endpoint = "https://document-intelligence-demo.cognitiveservices.azure.com/"
        credential = DefaultAzureCredential()
        self.client = DocumentIntelligenceClient(endpoint, credential)

    def extract_text(self, page: Document) -> Document:
        print(f"Running Azure Document Intelligence OCR on page {page.page_number}...")
        return page