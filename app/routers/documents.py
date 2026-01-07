from typing import Any, Dict, List

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi import status as http_status

from app.services.ingestion import extract_text_from_pdf, split_text_into_chunks
from app.services.rag import analyze_question_against_chunks


router = APIRouter()


@router.post("/analyze", summary="Upload a contract and ask a question.")
async def analyze_document(
    file: UploadFile = File(...),
    question: str = "What are the risky clauses in this contract?",
) -> Dict[str, Any]:
    """
    Ingest a PDF contract, index it into a vector store, and answer a question about it.

    This is a simple RAG pipeline:
    - Read PDF into text
    - Chunk the text
    - Embed + store chunks in a vector DB
    - Retrieve relevant chunks and call the LLM to answer the question
    """

    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported.",
        )

    raw_bytes = await file.read()
    text = extract_text_from_pdf(raw_bytes)
    if not text.strip():
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="Could not extract any text from the PDF.",
        )

    chunks: List[str] = split_text_into_chunks(text)
    answer, relevant_chunks = await analyze_question_against_chunks(question, chunks)

    return {
        "question": question,
        "answer": answer,
        "chunks_used": relevant_chunks,
        "num_chunks": len(chunks),
    }


