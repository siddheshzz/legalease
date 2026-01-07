from typing import List, Tuple

from langchain_core.documents import Document
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from app.config import get_settings


async def _get_llm() -> BaseChatModel:
    """Return the Groq chat model for answering questions (no OpenAI)."""

    settings = get_settings()
    if not settings.groq_api_key:
        raise RuntimeError("GROQ_API_KEY (groq_api_key) is not configured.")

    # You can change model_name if you prefer a different Groq model.
    return ChatGroq(
        groq_api_key=settings.groq_api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.0,
    )


async def analyze_question_against_chunks(
    question: str,
    chunks: List[str],
) -> Tuple[str, List[str]]:
    """
    Minimal RAG pipeline over in-memory chunks.

    NOTE: This currently uses simple cosine similarity in memory to keep the
    example self-contained. In production, you would:
    - Push embeddings to Pinecone/Supabase
    - Use a LangChain VectorStore-backed retriever instead of manual scoring
    """

    # Use a local HuggingFace model for embeddings, Groq only for the chat model.
    # This avoids any OpenAI usage entirely.
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Embed chunks
    docs = [Document(page_content=c) for c in chunks]
    doc_texts = [d.page_content for d in docs]
    doc_vectors = embeddings.embed_documents(doc_texts)

    # Embed question
    query_vector = embeddings.embed_query(question)

    # Compute simple cosine similarity scores (manual to avoid extra deps)
    def cosine_sim(a: List[float], b: List[float]) -> float:
        import math

        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        return dot / (norm_a * norm_b + 1e-10)

    scores = [cosine_sim(query_vector, vec) for vec in doc_vectors]

    # Take top-k chunks
    top_k = 5
    ranked = sorted(zip(scores, doc_texts), key=lambda x: x[0], reverse=True)[:top_k]
    relevant_chunks = [t for _, t in ranked]

    llm = await _get_llm()

    # Simple LangChain RAG chain: {context, question} -> LLM
    template = (
        "You are a contract risk analysis assistant.\n"
        "Use ONLY the provided context to answer the question.\n"
        "If the answer is not in the context, say you cannot find it.\n\n"
        "Context:\n{context}\n\nQuestion: {question}\nAnswer concisely and highlight any risky clauses."
    )

    chain = RunnablePassthrough.assign(
        context=lambda _: "\n\n---\n\n".join(relevant_chunks)
    ) | (lambda inputs: template.format(**inputs)) | llm

    result = await chain.ainvoke({"question": question})
    answer = result.content if hasattr(result, "content") else str(result)

    return answer, relevant_chunks


