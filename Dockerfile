# Use official lightweight Python 3.12 image
FROM python:3.12-slim as builder

WORKDIR /app

# Install system build dependencies for compile-on-install packages (like faiss if compiled from source, or other packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download and cache the SentenceTransformer embedding model during build
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-en-v1.5')"

# Final production stage
FROM python:3.12-slim

WORKDIR /app

# Copy python packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /root/.cache/huggingface /root/.cache/huggingface

# Copy project files
COPY app/ ./app
COPY frontend/ ./frontend

# Create non-root user and directories
RUN useradd -u 1000 appuser && \
    mkdir -p data/uploads data/faiss_indices && \
    chown -R appuser:appuser /app

USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
