from app.ocr.base import get_ocr_engine
from app.pipeline.state import PipelineState


def run_ocr_stage(state: PipelineState) -> PipelineState:
    """Runs OCR on the pages in the pipeline state using the specified OCR engine."""
    if state.get("ocr_needed") is False:
        return {"pages": state["pages"], "status": "ocr_skipped"}
    elif state.get("document_type") in ["pdf"]:
        engine = get_ocr_engine(state.get("ocr_engine", "tesseract"))
        for idx, page in enumerate(state["pages"]):
            if page.metadata.get("ocr_needed", False) is False:
                continue
            state["pages"][idx] = engine.extract_text(page)
    return {
        "pages": state["pages"],
        "status": "ocr_completed",
    }
