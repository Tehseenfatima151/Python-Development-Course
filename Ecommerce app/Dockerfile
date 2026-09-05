FROM python:3.11-slim

# Prevents Python from writing pyc files and enables unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (required for psycopg2-binary compilation on Linux)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and enable psycopg2-binary for the Linux container build,
# then install all dependencies.
COPY requirements.txt .
RUN sed 's/^# psycopg2-binary/psycopg2-binary/' requirements.txt > requirements_docker.txt \
 && pip install --no-cache-dir -r requirements_docker.txt \
 && rm requirements_docker.txt

# Copy application source
COPY . .

EXPOSE 5000

# Default command (overridden per service in docker-compose.yml)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "run:app"]
