from uuid import uuid4
from langgraph.graph import END, StateGraph

from app.pipeline.state import PipelineState
from app.pipeline.stages.detect_type import detect_document_type
from app.pipeline.stages.export import export_result
from app.pipeline.stages.extract_pages import extract_pages
from app.pipeline.stages.ocr import run_ocr_stage
from app.pipeline.stages.postprocess import postprocess_text
from app.pipeline.stages.preprocess import preprocess_pages


class OCRPipeline:
    def __init__(self) -> None:
        graph = StateGraph(PipelineState)
        graph.add_node("detect_type", detect_document_type)
        graph.add_node("extract_pages", extract_pages)
        graph.add_node("preprocess", preprocess_pages)
        graph.add_node("ocr", run_ocr_stage)
        graph.add_node("postprocess", postprocess_text)
        graph.add_node("export", export_result)
        graph.set_entry_point("detect_type")
        graph.add_edge("detect_type", "extract_pages")
        graph.add_edge("extract_pages", "preprocess")
        graph.add_edge("preprocess", "ocr")
        graph.add_edge("ocr", "postprocess")
        graph.add_edge("postprocess", "export")
        graph.add_edge("export", END)
        self.graph = graph.compile()
    
    def run(self, source_path: str, engine: str = "tesseract") -> PipelineState:
        initial_state: PipelineState = {
            "document_id": str(uuid4()),
            "source_path": source_path,
            "ocr_engine": engine,
            "status": "created",
            "metadata": {},
            "pages": [],
            "text": "",
        }
        return self.get_graph().invoke(initial_state)
