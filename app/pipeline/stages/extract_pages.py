from app.extractors.pdf.pymupdf import extract_pdf_documents
from app.pipeline.state import PipelineState


def extract_pages(state: PipelineState) -> PipelineState:
    if state.get("document_type") == "pdf":
        documents = extract_pdf_documents(state["source_path"])
        return {
            "pages": documents,
            "metadata": {"page_count": len(documents)},
            "status": "pages_extracted",
        }
    else:
        raise ValueError(f"Unsupported document type: {state.get('document_type')}")
