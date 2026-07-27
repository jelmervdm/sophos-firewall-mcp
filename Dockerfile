FROM python:3.11-slim

WORKDIR /app

# Install curl for container healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files & source code
COPY pyproject.toml requirements.txt README.md ./
COPY src/ ./src

# Install package dependencies
RUN pip install --no-cache-dir ".[router]"

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
