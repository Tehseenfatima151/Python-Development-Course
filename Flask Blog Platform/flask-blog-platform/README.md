# Flask Blog Platform

A complete, professional, full-stack blogging platform built with Python and Flask. Users can register, log in, write articles, comment on posts, and manage their profiles — all with proper authentication, authorization, and a clean Bootstrap 5 UI.

---

## Features

- **User Authentication** — Register, login, logout with secure password hashing
- **Auto-login after registration** — Users are logged in immediately after creating an account
- **Remember Me** — Persistent login sessions
- **Blog Post CRUD** — Create, read, update, and delete posts
- **Authorization** — Only the post author can edit or delete their own posts
- **Comment System** — Authenticated users can comment; only their own comments can be deleted
- **Profile Picture Upload** — Upload PNG/JPG/JPEG/WEBP avatars with unique filenames
- **Featured Post Images** — Optional image per blog post
- **Public Author Profiles** — View any author's post list
- **Flash Messages** — Bootstrap alerts for every user action
- **Custom Error Pages** — Friendly 404, 403, and 500 pages
- **CSRF Protection** — All forms use Flask-WTF tokens
- **Responsive UI** — Bootstrap 5 grid, cards, navbar, and modals
- **Delete Confirmation Modal** — Bootstrap modal before post deletion
- **SQLite Database** — Zero-config local database, auto-created on first run

---

## Technologies

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask 3 |
| ORM | Flask-SQLAlchemy (SQLite) |
| Authentication | Flask-Login, Werkzeug password hashing |
| Forms & Validation | Flask-WTF, WTForms |
| Frontend | Jinja2, Bootstrap 5, Bootstrap Icons |
| Environment | python-dotenv |

---

## Project Structure

```
flask-blog-platform/
│
├── main.py                  # App factory, models, forms, routes — everything
├── requirements.txt         # Python dependencies
├── .env                     # Secret key (not committed to git)
├── .env.example             # Template showing required variables
├── .gitignore
├── README.md
│
├── instance/
│   └── blog.db              # SQLite database (auto-created)
│
├── static/
│   ├── css/
│   │   └── styles.css       # Custom styles on top of Bootstrap
│   ├── img/
│   │   ├── default-avatar.svg
│   │   └── default-post.svg
│   └── uploads/
│       ├── profile_pics/    # User avatar uploads
│       └── post_images/     # Post featured image uploads
│
└── templates/
    ├── base.html            # Shared layout: navbar, flash messages, footer
    ├── index.html           # Homepage with hero + post cards
    ├── post.html            # Full article + comments
    ├── create_post.html     # New post form
    ├── edit_post.html       # Edit post form
    ├── register.html        # Registration form
    ├── login.html           # Login form
    ├── profile.html         # Logged-in user's own profile + settings
    ├── public_profile.html  # Public view of any author's profile
    ├── 404.html
    ├── 403.html
    └── 500.html
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd flask-blog-platform
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
copy .env.example .env      # Windows
cp .env.example .env        # macOS/Linux
```

Edit `.env` and set a strong secret key:

```
SECRET_KEY=your-very-long-random-secret-key
```

The secret key is used by Flask to sign session cookies and CSRF tokens. Never expose it or commit it to version control.

---

## Database

The project uses **SQLite** via **Flask-SQLAlchemy**. The database file (`instance/blog.db`) is created **automatically** the first time you run the application — no manual setup needed.

Three tables are created:
- `users` — registered accounts
- `posts` — blog articles
- `comments` — comments on posts

Cascade deletes are configured so that deleting a user removes their posts and comments, and deleting a post removes its comments.

---

## Running the Application

```bash
python main.py
```

Then open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

## Features Explanation

### Authentication
Passwords are hashed with Werkzeug's `generate_password_hash()` before being stored. `check_password_hash()` is used at login. Plain-text passwords are never saved. Flask-Login manages session state and the `@login_required` decorator protects private routes.

### CRUD
- **Create** — `/create-post` (login required)
- **Read** — `/` and `/post/<id>` (public)
- **Update** — `/edit-post/<id>` (author only, checked server-side)
- **Delete** — `/delete-post/<id>` via POST (author only, confirmed via modal)

### Comments
Submitted via POST to `/post/<id>/comment`. Deleted via POST to `/delete-comment/<id>`. Both routes verify ownership server-side.

### File Uploads
Uploaded files are renamed to a `uuid4` hex string to prevent collisions and path-traversal attacks. `secure_filename()` sanitises the name. Only PNG, JPG, JPEG, and WEBP are accepted. The 2 MB size limit is enforced by Flask's `MAX_CONTENT_LENGTH`.

### Database Relationships
```
User ──< Post ──< Comment
User ──< Comment
```

### Authorization
Every mutating route (edit, delete post/comment, profile update) checks `current_user.id` against the resource's owner ID. Mismatches return HTTP 403 via `abort(403)`.

### Bootstrap UI
The layout is fully responsive using Bootstrap 5's grid system. The navbar collapses on mobile. Cards, modals, badges, alerts, and Bootstrap Icons are used throughout.

---

