from app.ocr.base import get_ocr_engine
from app.pipeline.state import PipelineState


def run_ocr_stage(state: PipelineState) -> PipelineState:
    if state.get("ocr_needed") is False:
        return {"status": "ocr_skipped"}
    elif state.get("document_type") in ["pdf"]:
        for page in state["pages"]:
            if page.metadata.get("ocr_needed", False) is False:
                continue
            else:
                engine = get_ocr_engine(state["ocr_engine"])
                text = engine.extract_text(page)
                state["pages"][page.page_number - 1].text = text
    return {
        "pages": state["pages"],
        "status": "ocr_completed",
    }
