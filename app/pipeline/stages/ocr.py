from app.ocr.base import get_ocr_engine
from app.pipeline.state import PipelineState


def run_ocr_stage(state: PipelineState) -> PipelineState:
    if state.get("ocr_needed") is False:
        return {"status": "ocr_skipped"}
    elif state.get("document_type") in ["pdf"]:
        engine = get_ocr_engine(state["ocr_engine"])
        text = engine.extract_text(state["pages"])
    return {"text_dict": {"raw": text}, "status": "ocr_completed"}
