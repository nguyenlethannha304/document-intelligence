from app.pipeline.state import PipelineState
from app.storage.local import write_text_output


def export_result(state: PipelineState) -> PipelineState:
    text = state.get("text", "")
    output_path = write_text_output(state["document_id"], text)
    return {"output_path": str(output_path), "status": "completed"}
