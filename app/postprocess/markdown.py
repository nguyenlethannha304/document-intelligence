from app.postprocess.layout import normalize_layout
from app.postprocess.tables import preserve_tables


def to_markdown(text: str) -> str:
    return preserve_tables(normalize_layout(text))
