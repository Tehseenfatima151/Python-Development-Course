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
