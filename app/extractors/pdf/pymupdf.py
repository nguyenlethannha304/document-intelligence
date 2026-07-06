import pymupdf
from langchain_core.documents import Document


def extract_pdf_documents(path: str) -> list[Document]:
    pdf = pymupdf.open(path)
    documents: list[Document] = []
    try:
        for index, page in enumerate(pdf, start=1):
            documents.append(
                Document(
                    page_content=page.get_text().strip(),
                    metadata={"page": index, "source": path},
                )
            )
    finally:
        pdf.close()
    return documents
