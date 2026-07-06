from fastapi import APIRouter

router = APIRouter(tags=["jobs"])


@router.get("/jobs/{job_id}")
def get_job(job_id: str) -> dict[str, str]:
    return {"job_id": job_id, "status": "not-implemented"}
