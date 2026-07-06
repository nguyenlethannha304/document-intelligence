from fastapi import FastAPI

from app.api.jobs import router as jobs_router
from app.api.ocr import router as ocr_router
from app.api.upload import router as upload_router
from app.core.config import get_settings
from app.core.logging import configure_logging


configure_logging()
settings = get_settings()

app = FastAPI(title=settings.app_name, version=settings.app_version)
app.include_router(upload_router, prefix="/api")
app.include_router(ocr_router, prefix="/api")
app.include_router(jobs_router, prefix="/api")


@app.get("/health", tags=["system"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}
