"""
Development Entry Point

Run this file directly only for local development without Docker:
    python run.py

In production (and inside Docker) the application is served by Gunicorn:
    gunicorn "app:create_app()" --bind 0.0.0.0:5000
"""

import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    # debug=True is safe here because this file is never executed in production.
    app.run(host="0.0.0.0", port=port, debug=True)
