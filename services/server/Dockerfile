FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
#COPY ../../requirements.txt .
COPY requirements.txt .

#CPU based sentence transformers req (for embeddings stuff)
RUN pip3 install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code (file structure needs to seen from root of projcet then relative path)
#COPY services/server/app/ ./app/
COPY services/server/app ./app
COPY services/server/public/front-end/out/ ./public
COPY services/server/init.sql ./init.sql

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Expose port
EXPOSE 8000

# Start application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
