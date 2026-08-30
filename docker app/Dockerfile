# ---------------------------------------------------------------------------
# Stage 1 – builder
# Install Python dependencies into an isolated layer so that the final image
# only contains what the application actually needs.
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /install

# Copy only the requirements file first.
# Docker caches this layer; the pip install step is only re-run when
# requirements.txt changes, which speeds up rebuilds significantly.
COPY requirements.txt .

RUN pip install --upgrade pip --quiet \
    && pip install --no-cache-dir --prefix=/install/deps -r requirements.txt


# ---------------------------------------------------------------------------
# Stage 2 – final image
# Copy the installed packages and application source into a clean image.
# ---------------------------------------------------------------------------
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered stdout/stderr
# so container logs appear immediately.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy installed packages from the builder stage.
COPY --from=builder /install/deps /usr/local

# Create a non-root user and group for the application process.
# Running as root inside a container is a security anti-pattern.
RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser

# Copy the application source code.
COPY app/ ./app/
COPY run.py .

# Transfer ownership to the non-root user before switching.
RUN chown -R appuser:appgroup /app

USER appuser

# Expose the port the application listens on.
EXPOSE 5000

# Docker health check — calls /health every 30 seconds.
# --interval  how often to probe
# --timeout   time allowed for a single probe
# --retries   failures before marking the container unhealthy
# --start-period grace period after startup before probes count as failures
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=15s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" \
    || exit 1

# Production command: Gunicorn with 2 workers.
# Adjust --workers based on available CPU cores (2 * cores + 1 is a common rule).
CMD ["gunicorn", "app:create_app()", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "2", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
