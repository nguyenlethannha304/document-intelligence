from app.extractors.pdf.pymupdf import extract_pdf_documents
from app.pipeline.state import PipelineState

def extract_pages(state: PipelineState) -> PipelineState:
    """Extracts pages from the document based on its type and updates the pipeline state accordingly."""
    if state.get("document_type") == "pdf":
        documents = extract_pdf_documents(state["source_path"])
        return {
            "pages": documents,
            "metadata": {"page_count": len(documents)},
            "status": "pages_extracted",
            "ocr_needed": True if any(doc.metadata.get("ocr_needed", False) for doc in documents) else False,
        }
    else:
        raise ValueError(f"Unsupported document type: {state.get('document_type')}")
