from fastapi import APIRouter, HTTPException, Query

from app.core.exceptions import OCRPlatformError
from app.models.result import OCRResult
from app.pipeline.orchestrator import OCRPipeline

router = APIRouter(tags=["ocr"])
pipeline = OCRPipeline()


@router.post("/ocr", response_model=OCRResult)
def run_ocr(path: str = Query(...), engine: str = Query("azure_document_intelligence")) -> OCRResult:
    try:
        state = pipeline.run(source_path=path, engine=engine)
    except OCRPlatformError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return OCRResult(
        document_id=state["document_id"],
        source_path=state["source_path"],
        engine=state["ocr_engine"],
        page_count=len(state["pages"]),
        text=state.get("text_dict", {}).get("markdown") or state.get("text_dict", {}).get("raw", ""),
        status=state["status"],
    )
