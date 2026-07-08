from pathlib import Path

from app.core.exceptions import UnsupportedDocumentError
from app.pipeline.state import PipelineState


def detect_document_type(state: PipelineState) -> PipelineState:
    suffix = Path(state["source_path"]).suffix.lower()
    state["status"] = "detected"
    if suffix == ".pdf":
        state["document_type"] = "pdf"
    else:
        state["status"] = "error"
        raise UnsupportedDocumentError(
            "Only PDF documents are supported in this version."
        )
    return state
