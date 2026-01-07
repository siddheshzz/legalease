from io import BytesIO
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader


def extract_text_from_pdf(data: bytes) -> str:
    """Extract raw text from a PDF byte stream using pypdf."""

    buffer = BytesIO(data)
    reader = PdfReader(buffer)
    texts: List[str] = []
    for page in reader.pages:
        # pypdf returns "" for some scanned PDFs; OCR would be an optional extension.
        page_text = page.extract_text() or ""
        texts.append(page_text)
    return "\n\n".join(texts)


def split_text_into_chunks(text: str) -> List[str]:
    """Split long contract text into semantically meaningful chunks for RAG."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " "],
    )
    return splitter.split_text(text)


