FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /uvx /usr/local/bin/

WORKDIR /app
COPY pyproject.toml uv.lock* README.md ./
COPY src ./src

RUN uv sync --frozen --no-dev --extra ollama --extra ui 2>/dev/null || \
    uv sync --no-dev --extra ollama --extra ui

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app
COPY --from=builder /app /app

EXPOSE 7860

CMD ["websum", "ui", "--host", "0.0.0.0", "--port", "7860"]
