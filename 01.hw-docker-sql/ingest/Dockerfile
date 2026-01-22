# Base image
FROM python:3.13.11-slim

# Copy uv binary from official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set up working directory
WORKDIR /app

# Add virtual environment to PATH so we can use installed packages
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files
COPY pyproject.toml .python-version uv.lock ./

# Install deps inside container venv
RUN uv sync --locked

# copy your script and data
COPY ../main.py .
COPY ../data data/

# run it
ENTRYPOINT ["python", "main.py"]