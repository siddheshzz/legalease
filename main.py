"""
Legacy entrypoint.

For the API server, use:
    uv run legalease-api
or:
    uv run uvicorn app.main:app --reload
"""

from app.main import run


def main() -> None:
    run()


if __name__ == "__main__":
    main()
