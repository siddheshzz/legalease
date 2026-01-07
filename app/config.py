from functools import lru_cache
from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "LegalEase AI"
    environment: Literal["dev", "staging", "prod"] = "dev"
    debug: bool = True

    # Vector DB / RAG backend
    rag_backend: Literal["pinecone", "supabase"] = "pinecone"

    # Pinecone
    pinecone_api_key: Optional[str] = None
    pinecone_index_name: Optional[str] = None

    # LLM providers
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"

    google_api_key: Optional[str] = None
    google_model: str = "gemini-1.5-flash"

    groq_api_key: Optional[str] = None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings instance."""

    return Settings()


