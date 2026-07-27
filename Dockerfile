FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specifications
COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -e .

# Copy application source
COPY src/ ./src/
COPY entrypoint.sh ./

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
