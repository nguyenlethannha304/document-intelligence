from app.postprocess.markdown import to_markdown
from app.pipeline.state import PipelineState


def postprocess_text(state: PipelineState) -> PipelineState:
    for page in state["pages"]:
        text = to_markdown(page.page_content)
        state["text"] += text
    return {"text": state["text"], "status": "postprocessed"}