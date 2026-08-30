# 🐳 Dockerized Flask CI/CD App

[![CI/CD
Pipeline](https://github.com/Tehseenfatima151/Python-Development-Course/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Tehseenfatima151/Python-Development-Course/actions/workflows/ci-cd.yml)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-black)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Pytest](https://img.shields.io/badge/Tests-15%20passed-success)

A production-style Flask web application demonstrating **Docker
containerization, automated testing, Docker health checks, and a GitHub
Actions CI/CD pipeline** with Render deployment integration.

> **Deployment status:** CI/CD and Docker validation are working. The
> Render live deployment was not completed because Render required
> billing/card verification.

------------------------------------------------------------------------

## 🚀 Project Overview

This project keeps the business logic intentionally simple so the
engineering practices can take centre stage.

### What it demonstrates

-   🧩 Flask application factory pattern
-   🐳 Multi-stage Docker build
-   🔐 Non-root Docker container user
-   📦 Docker Compose for local development
-   🧪 Automated testing with pytest
-   ⚙️ GitHub Actions CI/CD pipeline
-   ❤️ `/health` endpoint for container/monitoring checks
-   🔑 Environment-variable based secret management
-   🚀 Gunicorn production WSGI server
-   ☁️ Render deployment configuration and deploy-hook integration

------------------------------------------------------------------------

## ✨ Features

  -----------------------------------------------------------------------
  Feature                             Details
  ----------------------------------- -----------------------------------
  Flask REST API                      `GET /` and `GET /health` endpoints

  Application Factory                 Clean, testable `create_app()`
                                      pattern

  Multi-stage Docker Build            Optimized image build with separate
                                      stages

  Non-root Container                  Runs as an unprivileged `appuser`

  Docker Health Check                 Configured in both `Dockerfile` and
                                      `docker-compose.yml`

  Docker Compose                      One-command local container setup

  pytest Suite                        15 automated tests

  GitHub Actions                      `test → docker-build → deploy`
                                      pipeline

  Smoke Tests                         Validates `/health` and `/` inside
                                      the CI container

  Gunicorn                            Production WSGI server instead of
                                      `flask run`

  Secret Management                   `.env` ignored; production secrets
                                      supplied through environment
                                      variables

  Render Integration                  `render.yaml` and deploy-hook
                                      workflow configuration
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 🏗️ Repository Structure

This project is maintained inside the existing
`Python-Development-Course` repository.

``` text
Python-Development-Course/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── day-81/
├── day-82/
├── ...
│
└── docker app/
    ├── app/
    │   ├── __init__.py
    │   ├── config.py
    │   └── routes.py
    │
    ├── tests/
    │   ├── __init__.py
    │   └── test_app.py
    │
    ├── Dockerfile
    ├── docker-compose.yml
    ├── render.yaml
    ├── requirements.txt
    ├── .env.example
    ├── .gitignore
    ├── .dockerignore
    ├── run.py
    └── README.md
```

The workflow is intentionally stored at the repository root because
GitHub Actions discovers workflows from `.github/workflows/`.

------------------------------------------------------------------------

## 🔄 CI/CD Architecture

``` text
Developer
   │
   │ git push
   ▼
GitHub Repository
   │
   ▼
GitHub Actions
   │
   ├── 1. TEST
   │      ├── Python 3.12
   │      ├── Install dependencies
   │      └── Run 15 pytest tests
   │
   ├── 2. DOCKER BUILD
   │      ├── Build Docker image
   │      ├── Start container
   │      ├── Test /health
   │      └── Test /
   │
   └── 3. DEPLOY
          └── Trigger Render Deploy Hook
              │
              ▼
          Render deployment
```

The `deploy` job runs only for a **push to `main`** and only after both
`test` and `docker-build` succeed.

------------------------------------------------------------------------

## 🛠️ Tech Stack

  Technology       Purpose
  ---------------- ------------------------
  Python 3.12      Runtime
  Flask 3.x        Web framework
  Gunicorn         Production WSGI server
  Docker           Containerization
  Docker Compose   Local orchestration
  GitHub Actions   CI/CD automation
  pytest           Automated testing
  Render           Deployment integration

------------------------------------------------------------------------

## 📋 Prerequisites

### Required for development/testing

-   Python 3.12+
-   Git
-   GitHub account

### Optional for local Docker execution

-   Docker Desktop

> Docker Desktop is **not required to validate the CI Docker build**
> because GitHub Actions runs the Docker build and smoke tests on its
> hosted runner. It is required if you want to build and run the
> containers locally with Docker Compose.

------------------------------------------------------------------------

## ⚙️ Local Setup

From the repository root:

``` bash
cd "docker app"
```

### 1. Create the environment file

``` bash
# macOS/Linux
cp .env.example .env

# Windows PowerShell
Copy-Item .env.example .env
```

Generate a strong secret:

``` bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Update `.env`:

``` env
FLASK_ENV=development
SECRET_KEY=<your-generated-key>
PORT=5000
APP_NAME=Dockerized Flask CI/CD App
```

> 🔐 **Never commit `.env`.** The real `.env` file is excluded through
> `.gitignore`. Only `.env.example` is committed.

------------------------------------------------------------------------

## 🐍 Run Without Docker

Useful for rapid development and testing.

From inside `docker app`:

``` bash
python -m venv .venv
```

### Windows

``` bash
.venv\Scripts\activate
```

### macOS/Linux

``` bash
source .venv/bin/activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

Run the development server:

``` bash
python run.py
```

Verify:

``` text
http://localhost:5000/
http://localhost:5000/health
```

------------------------------------------------------------------------

## 🐳 Run With Docker Compose

Docker Desktop must be installed and running for this section.

From inside `docker app`:

### Build

``` bash
docker compose build
```

### Start

``` bash
docker compose up
```

### Check health

``` bash
docker compose ps
```

Wait for the container status to become `healthy`.

### Stop

``` bash
docker compose down
```

------------------------------------------------------------------------

## 🧪 Testing

From inside `docker app`:

``` bash
pytest -v
```

### Verified result

``` text
15 passed
```

The test suite covers:

-   Root endpoint status
-   Root endpoint JSON response
-   Health endpoint status
-   Health response structure
-   Invalid/unknown routes
-   Application behavior and configuration

------------------------------------------------------------------------

## 🔌 API Endpoints

### `GET /`

Returns basic application information.

**Response:**

``` json
{
  "application": "Dockerized Flask CI/CD App",
  "status": "running",
  "environment": "development",
  "message": "Application is running successfully"
}
```

### `GET /health`

Lightweight health endpoint used by Docker and monitoring/deployment
systems.

**Response:**

``` json
{
  "status": "healthy"
}
```

------------------------------------------------------------------------

## 🔐 Security

Security considerations implemented in the project:

-   `.env` is excluded from Git through `.gitignore`
-   `SECRET_KEY` is loaded from an environment variable
-   No production secret is hard-coded in source code
-   Docker runs the application as a non-root `appuser`
-   CI smoke tests use a dedicated non-production test secret
-   Render deployment credentials are expected through GitHub Actions
    Secrets

### GitHub Actions Secret

The deployment job expects:

``` text
RENDER_DEPLOY_HOOK_URL
```

This should be stored under:

**GitHub → Repository Settings → Secrets and variables → Actions**

Never place the deploy-hook URL directly inside `ci-cd.yml`.

------------------------------------------------------------------------

## ⚙️ GitHub Actions CI/CD

Workflow:

``` text
.github/workflows/ci-cd.yml
```

### Job 1 --- `test`

Runs on project changes pushed to branches and on pull requests
targeting `main`.

Steps:

1.  Checkout repository
2.  Set up Python 3.12
3.  Restore pip cache
4.  Install `docker app/requirements.txt`
5.  Run `pytest -v`

### Job 2 --- `docker-build`

Runs only after `test` succeeds.

Steps:

1.  Set up Docker Buildx
2.  Build the Docker image
3.  Start a test container
4.  Wait for the application
5.  Verify `/health`
6.  Verify `/`
7.  Remove the test container

### Job 3 --- `deploy`

Runs only when:

``` text
push → main
```

and both previous jobs succeed.

It sends a `POST` request to the Render deploy hook stored in:

``` text
RENDER_DEPLOY_HOOK_URL
```

------------------------------------------------------------------------

## ✅ CI/CD Verification

  Check                               Result
  ----------------------------------- ---------------------------
  pytest --- 15 tests                 ✅ PASS
  GitHub Actions `test` job           ✅ PASS
  Docker image build                  ✅ PASS
  Docker smoke test                   ✅ PASS
  `GET /health`                       ✅ PASS
  `GET /`                             ✅ PASS
  Docker health check                 ✅ Configured
  Gunicorn                            ✅ Configured
  Non-root Docker user                ✅ Configured
  `.env` protection                   ✅ Configured
  `SECRET_KEY` environment variable   ✅ Configured
  Render integration                  ✅ Configured in workflow
  Live Render deployment              ⚠️ Not completed

------------------------------------------------------------------------

## ☁️ Deployment Status

### Render Integration

The project includes:

-   `render.yaml` Blueprint configuration
-   Dockerfile configured for production
-   Gunicorn startup
-   Docker health check
-   `/health` endpoint
-   GitHub Actions Render deploy-hook step

### Live deployment

The live Render deployment was **not completed** because Render required
billing/card verification.

No fake live URL is claimed.

The CI/CD deployment step remains ready to trigger a Render deployment
once a suitable Render service and deploy hook are available.

------------------------------------------------------------------------

## 🚀 How Deployment Would Work

``` text
1. Push code to main
          ↓
2. GitHub Actions runs tests
          ↓
3. Docker image builds
          ↓
4. Container smoke tests pass
          ↓
5. Deploy job runs
          ↓
6. Render Deploy Hook receives POST
          ↓
7. Render builds and starts the service
```

------------------------------------------------------------------------

## 🐛 Troubleshooting

### Port 5000 already in use

Windows:

``` bash
netstat -ano | findstr :5000
```

Stop Docker services:

``` bash
docker compose down
```

### Container exits immediately

``` bash
docker compose logs
docker compose ps
```

### Tests fail

Make sure you are inside the project directory:

``` bash
cd "docker app"
pytest -v
```

### Docker build fails

Try a clean rebuild:

``` bash
docker compose build --no-cache
```

### Render deploy job fails

Check that:

``` text
RENDER_DEPLOY_HOOK_URL
```

exists under:

**GitHub → Settings → Secrets and variables → Actions**

Do not paste the secret into the workflow file.

------------------------------------------------------------------------

## 🔮 Future Improvements

Possible production-level extensions:

-   📦 Push images to GHCR, Docker Hub, or AWS ECR
-   🌐 Add a staging environment
-   🗄️ Add PostgreSQL with SQLAlchemy/Alembic
-   ⚡ Add Redis and background task processing
-   📊 Add structured logging
-   🚨 Add monitoring and alerting
-   🔄 Add automated rollback
-   ☸️ Migrate to Kubernetes/Helm for larger deployments
-   🛡️ Add Docker image vulnerability scanning with Trivy or Snyk

------------------------------------------------------------------------

## 📄 License

MIT --- see [LICENSE](LICENSE) for details.

------------------------------------------------------------------------

## 👩‍💻 Project Focus

This project was built to demonstrate practical skills in:

**Flask • Docker • Docker Compose • GitHub Actions • CI/CD • Testing •
Security • Production Configuration**
