# Day 71 — Deploying Your Website

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

> **Note:** Day 71 is a deployment/DevOps day, not a new coding project. It takes an existing Flask app (e.g. the Day 69 blog capstone) and prepares it to run on a real production server instead of just `localhost`.

---

## 🧠 Concepts Covered

### 1. Why `python main.py` isn't enough for production
Flask's built-in development server (`app.run(debug=True)`) is:
- Single-threaded and slow under real traffic
- Insecure — `debug=True` can leak source code/secrets if it ever crashes publicly
- Not meant to stay running reliably 24/7

Production apps need a **WSGI server** (like Gunicorn) sitting in front of the Flask app instead.

### 2. WSGI servers — Gunicorn
Gunicorn ("Green Unicorn") is a production-grade WSGI HTTP server that runs your Flask app properly, handling multiple requests at once.

```bash
pip install gunicorn
gunicorn main:app
```
`main:app` means: *in the file `main.py`, run the Flask instance named `app`.*

### 3. Turning off Debug Mode
```python
if __name__ == '__main__':
    app.run(debug=False)   # never True in production
```
`debug=True` is only safe on your own local machine — it can expose an interactive Python console to anyone who triggers an error on a live site.

### 4. Environment variables for secrets
Hardcoded values like `SECRET_KEY`, API keys, and database URLs should never be committed to GitHub. Instead, read them from environment variables at runtime.

```python
import os

app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
MOVIE_DB_API_KEY = os.environ.get("TMDB_API_KEY")
```
Locally, these are set in a `.env` file (loaded via `python-dotenv`) which is listed in `.gitignore` (from Day 70) so it never gets pushed.

```python
from dotenv import load_dotenv
load_dotenv()
```

### 5. Switching from SQLite to a production database
SQLite (`sqlite:///data.db`) is a single file — fine for learning, but most hosting platforms use an ephemeral filesystem, meaning **the database can be wiped on every restart/deploy**. Production apps typically switch to **PostgreSQL**.

```python
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "sqlite:///data.db"  # fallback for local dev
)
```
Most hosting providers give you a `DATABASE_URL` environment variable automatically when you attach a PostgreSQL database.

### 6. A `Procfile` — telling the host how to run your app
Many hosting platforms look for a `Procfile` in the project root to know how to start the app.

```
web: gunicorn main:app
```

### 7. Pinning dependencies for the deploy environment
The host installs whatever is listed in `requirements.txt` — this must include *everything* the app needs, including `gunicorn` and `psycopg2` (PostgreSQL driver), which aren't needed for local dev.

```bash
pip freeze > requirements.txt
```

### 8. General deployment checklist
- [ ] `debug=False`
- [ ] Secrets moved to environment variables, `.env` in `.gitignore`
- [ ] Database strategy decided (SQLite only for prototypes; PostgreSQL for anything persistent)
- [ ] `Procfile` + `requirements.txt` (with `gunicorn`) present
- [ ] `.gitignore` excludes `venv/`, `instance/`, `.env`
- [ ] Code pushed to GitHub, connected to the hosting platform

---

## 📂 Files Added for Deployment
```
project/
├── main.py
├── requirements.txt      # now includes gunicorn (+ psycopg2 if using PostgreSQL)
├── Procfile               # web: gunicorn main:app
├── .env                   # local only — NEVER pushed (in .gitignore)
└── .gitignore
```

## ▶️ Running Locally vs Production
```bash
# Local development
python main.py

# Simulating production locally
gunicorn main:app
```

---

## ✅ Key Takeaways
- `app.run(debug=True)` is a local development tool only — production apps run behind a proper WSGI server like Gunicorn.
- Secrets (API keys, `SECRET_KEY`, database URLs) belong in environment variables, never hardcoded or committed to GitHub.
- SQLite is fine for learning, but its file can be wiped on hosting platforms with ephemeral storage — PostgreSQL is the standard production choice.
- A `Procfile` tells many hosting platforms exactly how to start your app.
- `requirements.txt` must be complete and accurate — missing a package like `gunicorn` will break the deploy even if it works fine locally.

## 📝 Practice Tasks
1. Add a `.env` file to one of your earlier Flask projects (e.g. Day 64's Top Movies) and move `MOVIE_DB_API_KEY` out of `main.py` into it using `python-dotenv`.
2. Write a `Procfile` for the Day 69 blog capstone project.
3. Test running one of your projects locally with `gunicorn main:app` instead of `python main.py`.
4. Review your GitHub repos — confirm no `.env` file or hardcoded API key was ever accidentally pushed.
