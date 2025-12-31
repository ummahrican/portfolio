# Use Python slim image
FROM python:3.12-slim

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Copy application
COPY . .

# Expose port
EXPOSE 5001

# Run the application
CMD ["uv", "run", "python", "main.py"]