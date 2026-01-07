from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.logging_config import configure_logging
from app.routers import documents


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup/shutdown hook for initializing heavy resources."""

    configure_logging()
    settings = get_settings()

    # TODO: initialize vector DB clients, LLM clients, etc. and attach to app.state
    # This keeps connections warm and re-usable.
    app.state.settings = settings

    yield

    # TODO: clean up connections if needed (vector DB, etc.).


app = FastAPI(
    title="LegalEase AI – Contract Analyzer",
    description="Upload contracts/agreements and get AI-powered risk analysis.",
    version="0.1.0",
    lifespan=lifespan,
)

# Allow local frontend dev (e.g. Vite on 5173) to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])


def run() -> None:
    """CLI entrypoint for running the API in development."""

    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


