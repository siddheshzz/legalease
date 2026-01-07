## LegalEase AI – Smart Contract/Document Analyzer

**Goal**: Upload long PDFs (rental agreements, employment contracts, etc.) and have the AI flag risky clauses or answer targeted questions like “Is there a 3‑month notice period?”.

This project is built with:
- **FastAPI** (backend API)
- **uv** (dependency + environment management)
- **LangChain** (RAG pipeline – loaders, splitters, retrievers, chains)
- **Vector search** (in-memory for now, extensible to Pinecone/Supabase)
- **OpenAI / Gemini** (LLM providers, configurable via environment)

### Project structure

```text
app/
  __init__.py
  main.py              # FastAPI app + lifespan
  config.py            # Pydantic settings (env-based)
  logging_config.py    # Structured logging
  routers/
    __init__.py
    documents.py       # /api/v1/documents/analyze
  services/
    __init__.py
    ingestion.py       # PDF reading + chunking
    rag.py             # Simple RAG pipeline
main.py                # Legacy entrypoint delegating to app.main:run
pyproject.toml         # uv-compatible project config
```

### Prerequisites

- Python 3.13 (as per `pyproject.toml`)
- `uv` installed (`pip install uv` or use the official installer)
- OpenAI (or Gemini) API key

### Setup with uv

```bash
cd /Users/siddheshz/Dev/Programing/python-projects/legalease-ai

# Install dependencies (dev extras included by default via tool.uv)
uv sync
```

Create an `.env` file in the project root:

```bash
cp .env.example .env  # after you create .env.example
```

Then edit `.env` with your keys:

```text
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
ENVIRONMENT=dev
```

### Running the API

Using the script entrypoint:

```bash
uv run legalease-api
```

Or directly with Uvicorn:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Swagger UI will be available at:

- `http://localhost:8000/docs`

### Using the analyzer

- Open Swagger UI.
- Call `POST /api/v1/documents/analyze`:
  - Upload a PDF in `file`.
  - Set `question`, e.g. `"Is there a 3 month notice period?"`.
- The response includes:
  - **answer**: LLM’s response constrained by retrieved chunks.
  - **chunks_used**: text fragments used as context.
  - **num_chunks**: total chunks from the document.

### Frontend (React + Vite)

A modern React frontend lives under `frontend/` and talks to the FastAPI backend.

#### Setup

```bash
cd /Users/siddheshz/Dev/Programing/python-projects/legalease-ai/frontend
npm install   # or pnpm/yarn if you prefer
```

#### Run the frontend

In one terminal, run the backend (from the project root):

```bash
uv run legalease-api
```

In another terminal, run the frontend dev server:

```bash
cd frontend
npm run dev
```

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`

The Vite dev server proxies `/api` to the FastAPI backend, and CORS is configured to allow the
frontend origin.

The UI lets you:

- Upload a PDF contract.
- Ask a natural language question.
- See the AI’s answer and the exact excerpts from the contract used as evidence.

#### Further qwork and scope we can impove

- **Vector DB**: replace in-memory similarity with Pinecone/Supabase retrievers.
- **Auth**: add authentication (e.g. JWT or API keys) for the endpoints.
- **Observability**: integrate structured logs with ELK/OpenTelemetry; add metrics.
- **Tests**: write `pytest` suites for ingestion, RAG logic, and API endpoints.
- **Deployment**: containerize with Docker, run via Gunicorn/Uvicorn behind Nginx or on a managed platform (Fly.io, Render, AWS, etc.).


