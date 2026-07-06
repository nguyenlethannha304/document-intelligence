from app.pipeline.state import PipelineState


def preprocess_pages(state: PipelineState) -> PipelineState:
    return {"pages": state["pages"], "status": "preprocessed"}
