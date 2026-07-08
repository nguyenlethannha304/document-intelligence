from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from app.core.exceptions import OCRPlatformError
from app.models.result import OCRResult
from app.pipeline.orchestrator import OCRPipeline
from app.storage.local import save_upload

router = APIRouter(tags=["ocr"])
pipeline = OCRPipeline()


@router.post("/ocr", response_model=OCRResult)
async def run_ocr(file: UploadFile = File(...)) -> OCRResult:
    _, storage_path = await save_upload(file)

    try:
        state = pipeline.run(source_path=str(storage_path))
    except OCRPlatformError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return OCRResult(
        document_id=state["document_id"],
        source_path=state["source_path"],
        engine=state.get("ocr_engine", ""),
        page_count=len(state["pages"]),
        text=state.get("text", ""),
        status=state["status"],
    )
