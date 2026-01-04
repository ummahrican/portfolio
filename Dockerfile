FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app
COPY pyproject.toml .
RUN uv sync --frozen --no-cache

COPY . .

ENV PATH="/app/.venv/bin:$PATH"
ENV PORT=5001
ENV RELOAD=false

EXPOSE 5001
CMD ["python", "main.py"]
