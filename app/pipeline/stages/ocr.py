from app.ocr.base import get_ocr_engine
from app.pipeline.state import PipelineState


def run_ocr_stage(state: PipelineState) -> PipelineState:
    """Runs OCR on the pages in the pipeline state using the specified OCR engine."""
    if state.get("document_type") in ["pdf"]:
        for ocr_engine_name in ["tesseract", "llm_ocr"]:
            engine = get_ocr_engine(ocr_engine_name)
            for idx, page in enumerate(state["pages"]):
                if page.metadata.get("ocr_needed", False) is False:
                    continue
                state["pages"][idx] = engine.extract_text(page)
    return state
