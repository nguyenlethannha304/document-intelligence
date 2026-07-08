from app.pipeline.state import PipelineState
from app.postprocess.markdown import to_markdown


def postprocess_text(state: PipelineState) -> PipelineState:
    for page in state["pages"]:
        text = to_markdown(page.page_content)
        state["text"] += text
    return {"text": state["text"], "status": "postprocessed"}
