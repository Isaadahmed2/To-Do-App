# Base image with Python 3.11
FROM python:3.11-slim

# Install curl for health check
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv for fast package management
RUN pip install uv

# Copy project files
COPY pyproject.toml ./

# Create virtual environment and install dependencies
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv pip install fastapi uvicorn pydantic

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p /app/logs

# Expose port 8000
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Run the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
