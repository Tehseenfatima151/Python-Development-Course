# Dockerized Flask CI/CD App

A production-style Python web application demonstrating professional containerization, automated testing, and a complete GitHub Actions CI/CD pipeline with deployment to Render.

---

## Project Overview

This project is intentionally simple in its business logic so that the engineering practices take centre stage. It shows how a real team would structure, test, containerize, and continuously deploy a Flask service.

**What it demonstrates:**

- Flask API using the **application factory pattern**
- **Docker** multi-stage build with a non-root user
- **Docker Compose** for a one-command local developer experience
- **Automated tests** with pytest and Flask's test client
- **GitHub Actions** CI/CD pipeline (test → build → deploy)
- **Health check endpoint** compatible with Docker, Render, and any monitoring tool
- **Environment variable security** — secrets never committed to source control
- **Production deployment** on Render using Gunicorn

---

## Features

| Feature | Detail |
|---|---|
| Flask REST API | `GET /` and `GET /health` endpoints |
| Application factory | Clean, testable `create_app()` pattern |
| Docker multi-stage build | Small final image, layer caching optimised |
| Non-root container user | Security best practice |
| Docker health check | Built into both Dockerfile and Compose |
| Docker Compose | Single-command local setup |
| pytest suite | 15 tests covering status codes and response structure |
| GitHub Actions | 3-job pipeline: test → docker-build → deploy |
| Render deployment | Blueprint-based, auto-deploys on push to main |
| Environment secrets | `.env.example` template, real `.env` never committed |

---

## Architecture

```
Developer (git push)
       │
       ▼
   GitHub repo
       │
       ▼
GitHub Actions
  ┌────┴─────┐
  │  test    │  install deps, run pytest (15 tests)
  └────┬─────┘
       │ passes
       ▼
  ┌────┴──────────┐
  │ docker-build  │  build image, smoke-test /health and /
  └────┬──────────┘
       │ passes  (main branch only)
       ▼
  ┌────┴──────┐
  │  deploy   │  POST to Render deploy hook
  └────┬──────┘
       │
       ▼
  Render platform
       │  pulls repo, builds Dockerfile, starts Gunicorn
       ▼
  Flask container
       │
       ├── GET /        → {"status":"running", ...}
       └── GET /health  → {"status":"healthy"}
```

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Runtime |
| Flask 3.x | Web framework |
| Gunicorn | Production WSGI server |
| Docker | Container runtime |
| Docker Compose | Local orchestration |
| GitHub Actions | CI/CD pipeline |
| pytest | Automated testing |
| Render | Cloud deployment platform |

---

## Prerequisites

- [Python 3.12+](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)
- [Git](https://git-scm.com/)
- A [GitHub](https://github.com) account
- A [Render](https://render.com) account (free tier works)

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/dockerized-flask-cicd.git
cd dockerized-flask-cicd
```

### 2. Create your local environment file

```bash
cp .env.example .env
```

Open `.env` and update `SECRET_KEY` with a real random value:

```bash
# Generate a strong key
python -c "import secrets; print(secrets.token_hex(32))"
```

Your `.env` should look like:

```env
FLASK_ENV=development
SECRET_KEY=<your-generated-key>
PORT=5000
```

> **Important:** `.env` is listed in `.gitignore`. Never commit it.

---

## Run Without Docker

Useful for rapid iteration during development.

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Start the development server
python run.py
```

Visit:
- http://localhost:5000/
- http://localhost:5000/health

---

## Run With Docker

### Build the image

```bash
docker compose build
```

### Start the container

```bash
docker compose up
```

The application is available at:
- http://localhost:5000/
- http://localhost:5000/health

### Check container health

```bash
docker compose ps
```

The `STATUS` column will show `healthy` once the health check passes (allow ~15 seconds after startup).

### Stop the container

```bash
docker compose down
```

---

## Testing

Run the full pytest suite (no Docker or running server needed):

```bash
pytest -v
```

Expected output:

```
tests/test_app.py::TestRootEndpoint::test_root_returns_200 PASSED
tests/test_app.py::TestRootEndpoint::test_root_returns_json PASSED
...
tests/test_app.py::TestHealthEndpoint::test_health_status_is_healthy PASSED
tests/test_app.py::TestNotFound::test_unknown_route_returns_404 PASSED

15 passed in Xs
```

---

## API Endpoints

### `GET /`

Returns application information.

**Response `200 OK`:**

```json
{
  "application": "Dockerized Flask CI/CD App",
  "status": "running",
  "environment": "development",
  "message": "Application is running successfully"
}
```

---

### `GET /health`

Lightweight health probe used by Docker, Render, and monitoring tools.

**Response `200 OK`:**

```json
{
  "status": "healthy"
}
```

---

## CI/CD Pipeline

The pipeline is defined in `.github/workflows/ci-cd.yml` and has three jobs.

### Job 1 — `test`

Triggered on every push and pull request.

1. Checks out the repository
2. Sets up Python 3.12 with pip caching
3. Installs `requirements.txt`
4. Runs `pytest -v` — the pipeline fails if any test fails

### Job 2 — `docker-build`

Runs only after `test` succeeds.

1. Sets up Docker Buildx
2. Builds the Docker image (with GitHub Actions cache for speed)
3. Starts the container and waits for it to accept requests
4. Asserts `GET /health` returns `{"status":"healthy"}`
5. Asserts `GET /` returns `{"status":"running"}`

### Job 3 — `deploy`

Runs only on pushes to `main`, after both previous jobs pass.

1. Sends a `POST` request to the Render deploy hook URL
2. Render pulls the latest commit, rebuilds the Docker image, and rolls out the new version

---

## Deployment to Render

### Option A — Render Blueprint (recommended)

1. Push this repository to GitHub.
2. Log in to [Render](https://render.com).
3. Click **New → Blueprint**.
4. Connect your GitHub account and select this repository.
5. Render reads `render.yaml` and creates the service automatically.
6. Set any environment variables that are marked `sync: false` in the Render dashboard.

### Option B — Manual service setup

1. Click **New → Web Service**.
2. Connect your GitHub repository.
3. Set **Runtime** to **Docker**.
4. Set **Dockerfile path** to `./Dockerfile`.
5. Set **Health check path** to `/health`.
6. Add the environment variables listed below.
7. Click **Create Web Service**.

After the first deploy, Render provides a public URL. Verify it:

```bash
curl https://<your-service>.onrender.com/health
# Expected: {"status":"healthy"}
```

---

## Environment Variables

### Local development

| Variable | Description | Example |
|---|---|---|
| `FLASK_ENV` | Runtime environment | `development` |
| `SECRET_KEY` | Session signing key | `<random hex>` |
| `PORT` | Listening port | `5000` |
| `APP_NAME` | Display name in root response | `Dockerized Flask CI/CD App` |

Copy `.env.example` to `.env` and fill in real values. Never commit `.env`.

### Production (Render)

Set these in the Render dashboard under **Environment**:

| Variable | Value |
|---|---|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | A strong random value (Render can auto-generate) |
| `PORT` | `10000` (Render's default; set automatically) |

### GitHub Actions secrets

The deploy job requires one repository secret:

| Secret | Where to get it |
|---|---|
| `RENDER_DEPLOY_HOOK_URL` | Render dashboard → your service → Settings → Deploy Hook |

Add it at: **GitHub repo → Settings → Secrets and variables → Actions → New repository secret**

#### Secret types explained

| Type | Where stored | Committed? | Use case |
|---|---|---|---|
| `.env.example` | Repository | ✅ Yes | Documents required keys with safe placeholder values |
| `.env` | Local machine only | ❌ No | Real local development values |
| GitHub Actions secrets | GitHub Settings | ❌ No | CI/CD credentials (deploy hooks, registry tokens) |
| Render environment vars | Render dashboard | ❌ No | Production secrets (`SECRET_KEY`, API keys) |

---

## Troubleshooting

### Port 5000 already in use

```bash
# Find the process using port 5000
# macOS/Linux:
lsof -i :5000
# Windows:
netstat -ano | findstr :5000

# Stop the container and restart
docker compose down
docker compose up
```

### Container exits immediately

```bash
# View container logs
docker compose logs web

# Check the container status
docker compose ps
```

### Tests fail with ImportError

```bash
# Make sure you are running pytest from the project root
cd dockerized-flask-cicd
pytest -v
```

### Docker image build fails

```bash
# Rebuild without cache to pick up fresh dependencies
docker compose build --no-cache
```

### Render deployment not triggering

1. Confirm `RENDER_DEPLOY_HOOK_URL` is saved in GitHub repository secrets (not environment variables).
2. Check the Actions run log for the `deploy` job — look for the HTTP status code in the curl output.
3. Verify the deploy hook URL is copied exactly from the Render dashboard (it starts with `https://api.render.com/deploy/...`).

### `/health` returns a non-200 response after deploy

- Allow 2–3 minutes for the container to start on Render's free tier.
- Check the Render service logs in the dashboard for startup errors.
- Confirm `SECRET_KEY` is set in the Render environment variables.

---

## Future Improvements

These are realistic next steps for a production-grade system — not implemented here to keep the project focused.

- **Docker image registry** — push images to Docker Hub, GitHub Container Registry (GHCR), or AWS ECR for auditability and faster deploys
- **Staging environment** — deploy feature branches to a staging Render service before merging to main
- **PostgreSQL** — add a database tier with SQLAlchemy and Alembic migrations
- **Redis** — add caching or a task queue (Celery)
- **Structured logging** — replace print-style logs with JSON-formatted logs using `structlog`
- **Monitoring & alerting** — integrate Sentry for error tracking or Prometheus + Grafana for metrics
- **Automated rollback** — trigger a rollback deploy if the health check fails post-deployment
- **Kubernetes** — migrate the Compose service definition to a Helm chart for larger-scale deployments
- **Docker image scanning** — add Trivy or Snyk to the CI pipeline to catch vulnerable dependencies

---

## License

MIT — see [LICENSE](LICENSE) for details.
