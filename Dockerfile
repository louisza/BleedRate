FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port (Railway will set PORT env var)
EXPOSE 8000

# Run the application using shell to allow PORT variable substitution
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
