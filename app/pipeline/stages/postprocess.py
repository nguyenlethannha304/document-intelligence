from app.postprocess.markdown import to_markdown
from app.pipeline.state import PipelineState


def postprocess_text(state: PipelineState) -> PipelineState:
    raw_text = state.get("text_dict", {}).get("raw", "")
    markdown_text = to_markdown(raw_text).strip()
    text_dict = dict(state.get("text_dict", {}))
    text_dict["markdown"] = markdown_text
    return {"text_dict": text_dict, "status": "postprocessed"}