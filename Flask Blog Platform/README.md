# 📝 Flask Blog Platform

A full-stack blogging platform built with **Python Flask** where users can create, manage, and interact with blog articles.

The application includes secure user authentication, blog post CRUD operations, categories, comments, reactions, profile pictures, search, and a personalized user dashboard.

---

## 🚀 Features

### 🔐 User Authentication
- User Registration
- User Login & Logout
- Secure password hashing
- Protected routes using Flask-Login
- User-specific access control

### 📝 Blog Posts
- Create new blog posts
- View published articles
- Edit existing posts
- Delete posts
- Featured image upload
- Post preview
- Article categories

### 🏷️ Categories
- Select categories while creating posts
- Predefined categories
- Create custom categories
- Category-based filtering
- Category displayed on articles

### 💬 Comments
- Logged-in users can comment on articles
- Users can delete their own comments
- Display commenter information
- Comments linked with users and posts

### ❤️ Reactions
- Multiple post reactions
- Reaction counts
- User-specific reactions
- Reaction activity tracked for dashboard

### 👤 User Profiles
- User profile pages
- Profile picture upload
- User information
- User's published articles

### 📊 User Dashboard
Logged-in users have a personalized dashboard containing:

- Total articles
- Total comments received
- Total comments written
- Total reactions
- My Articles
- Recent comments
- Recent reactions
- View, Edit and Delete article actions
- User-specific activity

### 🔎 Search
Users can search articles by:

- Title
- Subtitle
- Content
- Category

The search system also provides category filtering and a clear filter option.

### 🎨 Responsive UI
- Clean Bootstrap interface
- Responsive design
- Mobile-friendly layout
- Professional navigation
- Article cards
- User-friendly forms
- Responsive dashboard

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| Flask | Backend Web Framework |
| SQLAlchemy | ORM / Database Management |
| SQLite | Database |
| Flask-Login | User Authentication |
| WTForms | Form Handling & Validation |
| Jinja2 | Template Engine |
| Bootstrap | Responsive UI |
| HTML5 | Structure |
| CSS3 | Styling |
| JavaScript | Client-side Interactions |

---

## 📂 Project Structure

```text
Flask Blog Platform/
│
├── main.py
├── README.md
├── requirements.txt
│
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── uploads/
│   │   └── ...
│   └── images/
│       └── ...
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── dashboard.html
│   ├── create-post.html
│   ├── edit-post.html
│   └── post.html
│
└── instance/
    └── blog.db

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

📊 Dashboard

The dashboard gives each logged-in user an overview of their blogging activity.

Dashboard includes:
📄 Published Articles
💬 Comments Received
💭 Comments Written
❤️ Reactions
📝 My Articles
💬 Recent Comments
❤️ Recent Reactions

Each user can only access their own dashboard data.

🔎 Article Search

The navbar includes an article search feature.

Users can search using keywords such as:

Python
Flask
AI
Web Development
Career

They can also filter articles by category.

Example:

AI & Machine Learning
        ↓
Only AI/ML articles
        ↓
Clear Filter
        ↓
All Articles
🖼️ File Uploads

The platform supports:

Profile picture uploads
Blog featured image uploads

Uploaded files are handled through Flask's file upload functionality with appropriate validation.

🔒 Security

Security considerations implemented in the application include:

Password hashing
Login-required routes
User authorization
Protected post editing/deletion
Safe file upload handling
XSS-safe content rendering
Safe redirect handling
Upload size protection
CSRF protection through Flask-WTF
📱 Responsive Design

The interface is designed to work across:

💻 Desktop
📱 Mobile
📲 Tablet

Bootstrap's responsive grid and custom CSS are used to maintain a clean layout across different screen sizes.

🎯 Learning Objectives

This project helped strengthen practical knowledge of:

Flask application development
REST-style backend concepts
SQLAlchemy ORM
SQLite databases
Authentication & authorization
CRUD operations
Database relationships
Form validation
File uploads
Jinja2 templates
Bootstrap UI
Search & filtering
User dashboards
Comments & reactions
Full-stack application architecture
🎥 Project Demo

Demo Video:

https://drive.google.com/file/d/1tZTyxkW8_0dq8N3z8AZamsBPdl0H885X/view?usp=sharing

💻 GitHub Repository

Repository:
https://github.com/Tehseenfatima151/Python-Development-Course/tree/main/Flask%20Blog%20Platform
