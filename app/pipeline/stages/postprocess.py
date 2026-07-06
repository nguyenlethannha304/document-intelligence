from app.postprocess.markdown import to_markdown
from app.pipeline.state import PipelineState


def postprocess_text(state: PipelineState) -> PipelineState:
    text = state.get("text", "")
    markdown_text = to_markdown(text).strip()
    return {"text": text, "markdown": markdown_text, "status": "postprocessed"}