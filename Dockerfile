# Production Dockerfile with multi-stage build
# Optimized for minimal image size and fast startup

FROM python:3.12-slim AS builder

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache --no-dev

# Production stage
FROM python:3.12-slim AS production

# Security: Run as non-root user
RUN useradd -m -u 1000 app

WORKDIR /app

# Copy UV from builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --chown=app:app . .

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PORT=5001
ENV HOST=0.0.0.0
ENV RELOAD=false

# Switch to non-root user
USER app

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5001/health')" || exit 1

# Run the application
CMD ["python", "main.py"]