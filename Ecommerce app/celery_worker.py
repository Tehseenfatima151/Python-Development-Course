"""Celery worker entry point.

Usage:
    celery -A celery_worker.celery worker --loglevel=info
"""
from app import create_app
from app.extensions import celery

# Create the Flask app so the Celery instance gets fully configured
# (including the ContextTask that ensures tasks run inside an app context)
app = create_app()

# Import tasks so Celery discovers them
import app.tasks.email_tasks  # noqa: F401
