import pymupdf
from langchain_core.documents import Document


def _bboxes_intersect(a: tuple, b: tuple) -> bool:
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    return not (ax1 <= bx0 or bx1 <= ax0 or ay1 <= by0 or by1 <= ay0)


def _table_to_markdown(rows: list[list]) -> str:
    if not rows:
        return ""

    def _fmt_row(row: list[str]) -> str:
        cells = [str(cell).strip() if cell is not None else "" for cell in row]
        return "| " + " | ".join(cells) + " |"

    lines = [_fmt_row(rows[0]), "| " + " | ".join("---" for _ in rows[0]) + " |"]
    lines.extend(_fmt_row(row) for row in rows[1:])
    return "\n".join(lines)


def _convert_page_to_image(index, page) -> Document:
    pix = page.get_pixmap(dpi=150, alpha=False)
    image_bytes = pix.tobytes(
        "png"
    )  # real PNG file bytes, good for multipart UploadFile

    return Document(
        page_content="",
        metadata={
            "page": index,
            "source": page.parent.name,
            "num_tables": 0,
            "ocr_needed": True,
            "filename": f"page_{index}.png",
            "content_type": "image/png",
            "image_bytes": image_bytes,
        },
    )


def extract_pdf_documents(path: str) -> list[Document]:
    """
    Extract text and tables (as markdown) from each page of a PDF using pymupdf.
    If a page has no text or tables, it is converted to an image and marked for OCR.
    Returns a list of Document objects, one for each page.
    """
    documents: list[Document] = []
    print(f"Extracting pages from PDF: {path}")
    with pymupdf.open(path) as pdf:
        for index, page in enumerate(pdf, start=1):
            # Any embedded image disqualifies the page (treat as scan/image page)
            if page.get_images(full=True):
                documents.append(_convert_page_to_image(index, page))
                continue

            # Find tables first so their text can be excluded from the plain
            # text extraction below (avoids duplicating table content).
            tables = list(page.find_tables().tables)
            table_bboxes = [table.bbox for table in tables]

            text_blocks = []
            for x0, y0, x1, y1, block_text, _no, block_type in page.get_text("blocks"):
                if block_type != 0:  # skip non-text blocks
                    continue
                if any(_bboxes_intersect((x0, y0, x1, y1), b) for b in table_bboxes):
                    continue
                stripped = block_text.strip()
                if stripped:
                    text_blocks.append(stripped)

            content_parts = list(text_blocks)
            for t_index, table in enumerate(tables, start=1):
                md = _table_to_markdown(table.extract())
                if md:
                    content_parts.append(f"### Table {t_index}\n{md}")

            page_content = "\n\n".join(content_parts).strip()

            if not page_content:
                documents.append(_convert_page_to_image(index, page))
                continue
            documents.append(
                Document(
                    page_content=page_content,
                    metadata={
                        "page": index,
                        "source": path,
                        "num_tables": len(tables),
                        "ocr_needed": False,
                    },
                )
            )
    return documents
