# Base image
FROM python:3.13.11-slim

# Copy uv binary from official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set up working directory
WORKDIR /app

# Add virtual environment to PATH so we can use installed packages
ENV PATH="/app/.venv/bin:$PATH"

# Copy files from host
COPY pyproject.toml .python-version uv.lock ./

# Install dependencies from lock file (ensures reproducible builds)
RUN uv sync --locked

# Copy application code
COPY pipeline.py .

# Define entrypoint
ENTRYPOINT ["python", "pipeline.py"]