"""
Flask Blog Platform - Main Application File
============================================
This is the entry point of the Flask Blog Platform.
It contains all route definitions, database models, forms, and app configuration.
"""

import os
import re
import uuid
from datetime import datetime
from functools import wraps
from urllib.parse import urlparse

import markdown as md_lib
from dotenv import load_dotenv
from flask import (Flask, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from markupsafe import Markup, escape
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from wtforms import (BooleanField, EmailField, PasswordField, SelectField,
                     StringField, SubmitField, TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                Optional, ValidationError)

# ---------------------------------------------------------------------------
# Load environment variables from .env file
# ---------------------------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------------------------
# App Configuration
# ---------------------------------------------------------------------------

# Absolute path to the directory containing main.py — used to anchor all
# file paths so the app works correctly regardless of the working directory
# from which it is launched (e.g. `python main.py` or `python flask-blog-platform/main.py`).
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, instance_path=os.path.join(BASE_DIR, "instance"))

# Secret key — loaded from environment variable (never hard-coded)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "fallback-dev-key-change-in-production"
)

# SQLite database — absolute path so it always resolves to instance/blog.db
# next to main.py, regardless of CWD.
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + os.path.join(BASE_DIR, "instance", "blog.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# File upload settings — absolute paths anchored to BASE_DIR
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads", "profile_pics")
POST_IMG_FOLDER = os.path.join(BASE_DIR, "static", "uploads", "post_images")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB max upload

# ---------------------------------------------------------------------------
# Extensions
# ---------------------------------------------------------------------------
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"
login_manager.login_message = "Please log in to access this page."


# ---------------------------------------------------------------------------
# Jinja2 custom filter: nl2br
# Converts plain-text newlines to <br> tags safely (no XSS).
# ---------------------------------------------------------------------------
@app.template_filter("nl2br")
def nl2br_filter(value):
    """Escape the value then replace newlines with <br> tags."""
    escaped = escape(value)
    return Markup(escaped.replace("\n", "<br>\n"))


@app.template_filter("render_markdown")
def render_markdown_filter(value):
    """
    Render a Markdown string to safe HTML.
    Enables: headings, bold, italic, bullet lists, numbered lists,
    blockquotes, code blocks, horizontal rules, and links.
    The output is marked Markup so Jinja2 does not double-escape it.
    """
    if not value:
        return Markup("")
    html = md_lib.markdown(
        value,
        extensions=["extra", "nl2br", "sane_lists"],
    )
    return Markup(html)


# ---------------------------------------------------------------------------
# Helper: ensure upload folders exist
# ---------------------------------------------------------------------------
def ensure_upload_folders():
    """Create upload directories if they do not exist."""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(POST_IMG_FOLDER, exist_ok=True)


# ---------------------------------------------------------------------------
# Helper: validate safe redirect target (prevent open redirect)
# ---------------------------------------------------------------------------
def is_safe_url(target):
    """
    Return True only if the redirect target is a relative path on the same host.
    Prevents open-redirect attacks via the ?next= parameter.
    """
    if not target:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(target)
    # Accept relative URLs (no scheme/netloc) or same-host absolute URLs
    return test_url.scheme in ("", "http", "https") and (
        test_url.netloc == "" or test_url.netloc == ref_url.netloc
    )


# ---------------------------------------------------------------------------
# Helper: check allowed file extension
# ---------------------------------------------------------------------------
def allowed_file(filename):
    """Return True if the filename has an allowed image extension."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ---------------------------------------------------------------------------
# Helper: save uploaded profile picture
# ---------------------------------------------------------------------------
def save_profile_picture(file_storage):
    """
    Save an uploaded profile picture with a unique filename.
    Returns the filename (not the full path).
    """
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    ext = file_storage.filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    safe_name = secure_filename(unique_name)
    save_path = os.path.join(UPLOAD_FOLDER, safe_name)
    file_storage.save(save_path)
    return safe_name


# ---------------------------------------------------------------------------
# Helper: save uploaded post image
# ---------------------------------------------------------------------------
def save_post_image(file_storage):
    """
    Save a post featured image with a unique filename.
    Returns the filename (not the full path).
    """
    os.makedirs(POST_IMG_FOLDER, exist_ok=True)
    ext = file_storage.filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    safe_name = secure_filename(unique_name)
    file_storage.save(os.path.join(POST_IMG_FOLDER, safe_name))
    return safe_name


# ===========================================================================
# DATABASE MODELS
# ===========================================================================

class User(UserMixin, db.Model):
    """
    Represents a registered user.

    Relationships:
        - User has many Posts  (one-to-many)
        - User has many Comments (one-to-many)
    """
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=False)
    password      = db.Column(db.String(256), nullable=False)   # hashed only
    profile_image = db.Column(db.String(200), nullable=True)    # filename
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships — cascade ensures child rows are removed with the parent
    posts    = db.relationship("Post",    backref="author", lazy=True,
                               cascade="all, delete-orphan")
    comments = db.relationship("Comment", backref="author", lazy=True,
                               cascade="all, delete-orphan")

    @property
    def avatar_url(self):
        """Return the URL for the user's profile picture, or a default avatar."""
        if self.profile_image:
            return url_for(
                "static", filename=f"uploads/profile_pics/{self.profile_image}"
            )
        return url_for("static", filename="img/default-avatar.svg")

    def __repr__(self):
        return f"<User {self.email}>"


class Category(db.Model):
    """
    Represents a blog post category.
    Categories are created by users when writing a post.
    Each post belongs to exactly one category.
    """
    __tablename__ = "categories"

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    posts = db.relationship("Post", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


# Predefined categories seeded on first run
PREDEFINED_CATEGORIES = [
    "Technology",
    "Python",
    "Web Development",
    "AI & Machine Learning",
    "Software Engineering",
    "Programming",
    "Tutorials",
    "Career",
    "Other",
]


class Post(db.Model):
    """
    Represents a blog post.

    Relationships:
        - Post belongs to a User (many-to-one)
        - Post belongs to a Category (many-to-one)
        - Post has many Comments (one-to-many)
    """
    __tablename__ = "posts"

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    subtitle    = db.Column(db.String(300), nullable=True)
    body        = db.Column(db.Text, nullable=False)
    image       = db.Column(db.String(200), nullable=True)       # filename
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow)
    author_id   = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # category_id is nullable so existing posts without a category don't break
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)

    # Post Reaction counts
    likes_count          = db.Column(db.Integer, default=0, nullable=False)
    dislikes_count       = db.Column(db.Integer, default=0, nullable=False)
    hearts_count         = db.Column(db.Integer, default=0, nullable=False)
    congratulations_count = db.Column(db.Integer, default=0, nullable=False)

    # Relationships
    comments = db.relationship("Comment", backref="post", lazy=True,
                               cascade="all, delete-orphan")

    @property
    def image_url(self):
        """Return URL for the post's featured image, or a placeholder."""
        if self.image:
            return url_for(
                "static", filename=f"uploads/post_images/{self.image}"
            )
        return url_for("static", filename="img/default-post.svg")

    @property
    def preview(self):
        """Return a plain-text preview of the post body (first 200 chars)."""
        # Strip markdown syntax, then strip any residual HTML tags
        plain = re.sub(r"#+ ", "", self.body)          # headings
        plain = re.sub(r"\*\*(.+?)\*\*", r"\1", plain) # bold
        plain = re.sub(r"\*(.+?)\*",     r"\1", plain) # italic
        plain = re.sub(r"`(.+?)`",       r"\1", plain) # inline code
        plain = re.sub(r"^[-*+] ",       "",    plain, flags=re.MULTILINE)  # bullets
        plain = re.sub(r"<[^>]+>",       "",    plain) # any HTML tags
        plain = plain.strip()
        return plain[:200] + "…" if len(plain) > 200 else plain

    def __repr__(self):
        return f"<Post {self.title}>"


class Comment(db.Model):
    """
    Represents a comment on a blog post.

    Relationships:
        - Comment belongs to a User (many-to-one)
        - Comment belongs to a Post (many-to-one)
    """
    __tablename__ = "comments"

    id         = db.Column(db.Integer, primary_key=True)
    text       = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id    = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    def __repr__(self):
        return f"<Comment by user {self.user_id} on post {self.post_id}>"


# ---------------------------------------------------------------------------
# Template context: categories for the navbar search filter
# ---------------------------------------------------------------------------
@app.context_processor
def inject_search_categories():
    """Expose the current database categories to the navbar search UI."""
    return {
        "search_categories": Category.query.order_by(Category.name.asc()).all()
    }


# ---------------------------------------------------------------------------
# Flask-Login user loader
# ---------------------------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    """Tell Flask-Login how to load a user by primary key."""
    return db.session.get(User, int(user_id))


# ===========================================================================
# FORMS (WTForms + Flask-WTF)
# ===========================================================================

class RegistrationForm(FlaskForm):
    """Form for creating a new user account."""
    name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    email = EmailField(
        "Email Address",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    profile_image = FileField(
        "Profile Picture (optional)",
        validators=[
            Optional(),
            FileAllowed(list(ALLOWED_EXTENSIONS),
                        "Images only (png, jpg, jpeg, webp)."),
        ],
    )
    submit = SubmitField("Create Account")

    def validate_email(self, field):
        """Ensure the email address is not already registered."""
        user = User.query.filter_by(email=field.data.lower()).first()
        if user:
            raise ValidationError(
                "That email is already registered. Please log in."
            )


class LoginForm(FlaskForm):
    """Form for user login."""
    email    = EmailField("Email Address",
                          validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit   = SubmitField("Log In")


class PostForm(FlaskForm):
    """Form for creating and editing blog posts."""
    title    = StringField("Title",
                           validators=[DataRequired(), Length(min=3, max=200)])
    subtitle = StringField("Subtitle",
                           validators=[Optional(), Length(max=300)])
    body     = TextAreaField("Content",
                             validators=[DataRequired(), Length(min=10)])

    # Category — user picks from existing or chooses "create new"
    category_id = SelectField(
        "Category",
        coerce=str,       # kept as string; we convert to int or handle new-name in route
        validators=[DataRequired(message="Please select or create a category.")],
    )
    # New category name — only required when category_id == "__new__"
    new_category = StringField(
        "New Category Name",
        validators=[Optional(), Length(max=100)],
    )

    image    = FileField(
        "Featured Image (optional)",
        validators=[
            Optional(),
            FileAllowed(list(ALLOWED_EXTENSIONS), "Images only."),
        ],
    )
    submit = SubmitField("Publish Post")


class CommentForm(FlaskForm):
    """Form for submitting a comment on a post."""
    text   = TextAreaField("Your Comment",
                           validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField("Post Comment")


class ProfileForm(FlaskForm):
    """Form for updating the user's profile."""
    name          = StringField("Full Name",
                                validators=[DataRequired(), Length(min=2, max=100)])
    profile_image = FileField(
        "Update Profile Picture",
        validators=[
            Optional(),
            FileAllowed(list(ALLOWED_EXTENSIONS), "Images only."),
        ],
    )
    current_password = PasswordField(
        "Current Password (required to change password)",
        validators=[Optional()],
    )
    new_password = PasswordField(
        "New Password",
        validators=[Optional(), Length(min=6)],
    )
    confirm_new_password = PasswordField(
        "Confirm New Password",
        validators=[
            Optional(),
            EqualTo("new_password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Update Profile")


# ===========================================================================
# ROUTES — Authentication
# ===========================================================================

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Registration page.
    GET  → show the registration form.
    POST → validate, create user, log them in, redirect to home.
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash password — never store plain text
        hashed_pw = generate_password_hash(form.password.data)

        # Handle optional profile picture
        pic_filename = None
        if form.profile_image.data and form.profile_image.data.filename:
            pic_filename = save_profile_picture(form.profile_image.data)

        user = User(
            name=form.name.data.strip(),
            email=form.email.data.lower().strip(),
            password=hashed_pw,
            profile_image=pic_filename,
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)   # automatically log in after registration
        flash("Account created successfully! Welcome to the blog.", "success")
        return redirect(url_for("index"))

    return render_template("register.html", form=form, title="Register")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login page.
    GET  → show login form.
    POST → validate credentials, log in, redirect.
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data.lower().strip()
        ).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login successful! Welcome back.", "success")
            # Safe redirect: only follow ?next= if it's a relative path
            next_page = request.args.get("next")
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for("index"))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template("login.html", form=form, title="Log In")


@app.route("/logout")
@login_required
def logout():
    """Log the current user out and redirect to home."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


# ===========================================================================
# ROUTES — Blog Posts (CRUD)
# ===========================================================================

@app.route("/")
@app.route("/home")
def index():
    """
    Homepage — shows all blog posts in reverse chronological order.
    Supports ?q= text search and ?category= category filtering.
    Accessible by all users (guests and authenticated).
    """
    q = request.args.get("q", "").strip()
    selected_category_id = request.args.get("category", type=int)
    selected_category = (
        db.session.get(Category, selected_category_id)
        if selected_category_id else None
    )

    posts_query = Post.query
    if q:
        # Case-insensitive search across title, subtitle, body, and category name
        like = f"%{q}%"
        posts_query = (
            posts_query
            .outerjoin(Category, Post.category_id == Category.id)
            .filter(
                db.or_(
                    Post.title.ilike(like),
                    Post.subtitle.ilike(like),
                    Post.body.ilike(like),
                    Category.name.ilike(like),
                )
            )
        )

    if selected_category_id:
        posts_query = posts_query.filter(Post.category_id == selected_category_id)

    posts = posts_query.order_by(Post.created_at.desc()).all()
    return render_template(
        "index.html",
        posts=posts,
        title="Home",
        search_query=q,
        selected_category=selected_category,
        search_active=bool(q or selected_category_id),
    )


@app.route("/post/<int:post_id>")
def view_post(post_id):
    """
    Individual post page.
    Shows the full article, author info, comments, and a comment form
    (only if the user is authenticated).
    """
    post = db.session.get(Post, post_id)
    if post is None:
        abort(404)
    comments = (
        Comment.query
        .filter_by(post_id=post_id)
        .order_by(Comment.created_at.asc())
        .all()
    )
    form = CommentForm()
    return render_template(
        "post.html", post=post, comments=comments,
        form=form, title=post.title
    )


@app.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    """
    Create a new blog post.
    Only authenticated users can access this route.
    """
    form = PostForm()
    # Populate category choices: existing categories + "Create New"
    categories = Category.query.order_by(Category.name).all()
    form.category_id.choices = (
        [("", "— Select a category —")] +
        [(str(c.id), c.name) for c in categories] +
        [("__new__", "+ Create New Category")]
    )

    if form.validate_on_submit():
        # Resolve category
        cat_val = form.category_id.data
        if cat_val == "__new__":
            new_name = form.new_category.data.strip() if form.new_category.data else ""
            if not new_name:
                form.new_category.errors.append("Please enter a category name.")
                return render_template("create_post.html", form=form,
                                       title="New Post", legend="Create New Post")
            # Get or create the new category
            cat = Category.query.filter_by(name=new_name).first()
            if not cat:
                cat = Category(name=new_name)
                db.session.add(cat)
                db.session.flush()   # get the id before commit
            category_id = cat.id
        elif cat_val == "" or cat_val is None:
            form.category_id.errors.append("Please select a category.")
            return render_template("create_post.html", form=form,
                                   title="New Post", legend="Create New Post")
        else:
            category_id = int(cat_val)

        img_filename = None
        if form.image.data and form.image.data.filename:
            img_filename = save_post_image(form.image.data)

        post = Post(
            title=form.title.data.strip(),
            subtitle=form.subtitle.data.strip() if form.subtitle.data else None,
            body=form.body.data,
            image=img_filename,
            author_id=current_user.id,
            category_id=category_id,
        )
        db.session.add(post)
        db.session.commit()
        flash("Post created successfully!", "success")
        return redirect(url_for("view_post", post_id=post.id))

    return render_template("create_post.html", form=form,
                           title="New Post", legend="Create New Post")


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    """
    Edit an existing blog post.
    Only the author of the post is allowed to edit it.
    """
    post = db.session.get(Post, post_id)
    if post is None:
        abort(404)

    # Authorization: only the author may edit
    if post.author_id != current_user.id:
        abort(403)

    form = PostForm()
    categories = Category.query.order_by(Category.name).all()
    form.category_id.choices = (
        [("", "— Select a category —")] +
        [(str(c.id), c.name) for c in categories] +
        [("__new__", "+ Create New Category")]
    )

    if request.method == "GET":
        form.title.data       = post.title
        form.subtitle.data    = post.subtitle
        form.body.data        = post.body
        form.category_id.data = str(post.category_id) if post.category_id else ""

    if form.validate_on_submit():
        cat_val = form.category_id.data
        if cat_val == "__new__":
            new_name = form.new_category.data.strip() if form.new_category.data else ""
            if not new_name:
                form.new_category.errors.append("Please enter a category name.")
                return render_template("edit_post.html", form=form, post=post,
                                       title="Edit Post", legend="Edit Post")
            cat = Category.query.filter_by(name=new_name).first()
            if not cat:
                cat = Category(name=new_name)
                db.session.add(cat)
                db.session.flush()
            post.category_id = cat.id
        elif cat_val == "" or cat_val is None:
            form.category_id.errors.append("Please select a category.")
            return render_template("edit_post.html", form=form, post=post,
                                   title="Edit Post", legend="Edit Post")
        else:
            post.category_id = int(cat_val)

        if form.image.data and form.image.data.filename:
            post.image = save_post_image(form.image.data)

        post.title      = form.title.data.strip()
        post.subtitle   = form.subtitle.data.strip() if form.subtitle.data else None
        post.body       = form.body.data
        post.updated_at = datetime.utcnow()

        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for("view_post", post_id=post.id))

    return render_template("edit_post.html", form=form, post=post,
                           title="Edit Post", legend="Edit Post")


@app.route("/delete-post/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        abort(404)

    if post.author_id != current_user.id:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully!", "success")
    return redirect(url_for("index"))


@app.route("/post/<int:post_id>/react", methods=["POST"])
def react_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return {"error": "Post not found"}, 404

    data = request.get_json() or {}
    reaction = data.get("reaction")
    action = data.get("action", "add")

    if reaction not in ["like", "dislike", "heart", "congratulations"]:
        return {"error": "Invalid reaction type"}, 400

    delta = 1 if action == "add" else -1

    if reaction == "like":
        post.likes_count = max(0, (post.likes_count or 0) + delta)
    elif reaction == "dislike":
        post.dislikes_count = max(0, (post.dislikes_count or 0) + delta)
    elif reaction == "heart":
        post.hearts_count = max(0, (post.hearts_count or 0) + delta)
    elif reaction == "congratulations":
        post.congratulations_count = max(0, (post.congratulations_count or 0) + delta)

    db.session.commit()

    return {
        "success": True,
        "likes": post.likes_count or 0,
        "dislikes": post.dislikes_count or 0,
        "hearts": post.hearts_count or 0,
        "congratulations": post.congratulations_count or 0,
    }


@app.route("/post/<int:post_id>/comment", methods=["POST"])
@login_required
def add_comment(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        abort(404)

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            text=form.text.data.strip(),
            user_id=current_user.id,
            post_id=post.id,
        )
        db.session.add(comment)
        db.session.commit()
        flash("Comment added!", "success")
    else:
        flash("Comment cannot be empty.", "warning")
    return redirect(url_for("view_post", post_id=post_id))


@app.route("/delete-comment/<int:comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    if comment is None:
        abort(404)

    if comment.user_id != current_user.id:
        abort(403)

    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted.", "info")
    return redirect(url_for("view_post", post_id=post_id))


@app.route("/dashboard")
@login_required
def dashboard():
    """
    User Dashboard for logged-in users.
    Displays user's own statistics, articles, recent comments, and reaction summary.
    """
    user_posts = (
        Post.query
        .filter_by(author_id=current_user.id)
        .order_by(Post.created_at.desc())
        .all()
    )

    total_articles = len(user_posts)
    post_ids = [p.id for p in user_posts]
    
    if post_ids:
        comments_received = (
            Comment.query
            .filter(Comment.post_id.in_(post_ids))
            .order_by(Comment.created_at.desc())
            .all()
        )
    else:
        comments_received = []

    total_comments_received = len(comments_received)

    comments_written = (
        Comment.query
        .filter_by(user_id=current_user.id)
        .all()
    )
    total_comments_written = len(comments_written)

    total_reactions = sum(
        (p.likes_count or 0) + (p.dislikes_count or 0) +
        (p.hearts_count or 0) + (p.congratulations_count or 0)
        for p in user_posts
    )

    reacted_posts = [
        p for p in user_posts
        if ((p.likes_count or 0) + (p.dislikes_count or 0) +
            (p.hearts_count or 0) + (p.congratulations_count or 0)) > 0
    ]

    form = PostForm()

    return render_template(
        "dashboard.html",
        title="Dashboard",
        posts=user_posts,
        total_articles=total_articles,
        total_comments_received=total_comments_received,
        total_comments_written=total_comments_written,
        total_reactions=total_reactions,
        recent_comments=comments_received[:10],
        reacted_posts=reacted_posts,
        form=form,
    )


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm()

    if form.validate_on_submit():
        current_user.name = form.name.data.strip()

        # Handle optional new profile picture
        if form.profile_image.data and form.profile_image.data.filename:
            current_user.profile_image = save_profile_picture(
                form.profile_image.data
            )

        # Handle optional password change
        if form.new_password.data:
            if not form.current_password.data:
                flash(
                    "Please enter your current password to set a new one.",
                    "warning",
                )
                return redirect(url_for("profile"))
            if not check_password_hash(
                current_user.password, form.current_password.data
            ):
                flash("Current password is incorrect.", "danger")
                return redirect(url_for("profile"))
            current_user.password = generate_password_hash(form.new_password.data)

        db.session.commit()
        flash("Profile updated!", "success")
        return redirect(url_for("profile"))

    elif request.method == "GET":
        form.name.data = current_user.name

    user_posts = (
        Post.query
        .filter_by(author_id=current_user.id)
        .order_by(Post.created_at.desc())
        .all()
    )
    return render_template(
        "profile.html", form=form, posts=user_posts, title="My Profile"
    )


@app.route("/user/<int:user_id>")
def public_profile(user_id):
    """
    Public profile page showing a user's posts.
    Accessible by everyone.
    """
    user = db.session.get(User, user_id)
    if user is None:
        abort(404)
    posts = (
        Post.query
        .filter_by(author_id=user_id)
        .order_by(Post.created_at.desc())
        .all()
    )
    return render_template(
        "public_profile.html", user=user, posts=posts,
        title=f"{user.name}'s Profile"
    )


# ===========================================================================
# ERROR HANDLERS
# ===========================================================================

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 — Page Not Found."""
    return render_template("404.html", title="Page Not Found"), 404


@app.errorhandler(403)
def forbidden(e):
    """Custom 403 — Forbidden / Not Authorized."""
    return render_template("403.html", title="Access Denied"), 403


@app.errorhandler(413)
def request_entity_too_large(e):
    """Custom 413 — Uploaded file exceeds the 2 MB limit."""
    flash("File too large. Maximum upload size is 2 MB.", "danger")
    return redirect(request.referrer or url_for("index"))


@app.errorhandler(500)
def internal_error(e):
    """Custom 500 — Internal Server Error."""
    db.session.rollback()
    return render_template("500.html", title="Server Error"), 500


def ensure_reaction_columns():
    """Ensure SQLite posts table contains reaction columns."""
    from sqlalchemy import inspect, text
    try:
        inspector = inspect(db.engine)
        if "posts" in inspector.get_table_names():
            columns = [c["name"] for c in inspector.get_columns("posts")]
            with db.engine.connect() as conn:
                for col in ["likes_count", "dislikes_count", "hearts_count", "congratulations_count"]:
                    if col not in columns:
                        conn.execute(text(f"ALTER TABLE posts ADD COLUMN {col} INTEGER DEFAULT 0"))
                conn.commit()
    except Exception as err:
        print("Migration check info:", err)


# ===========================================================================
# APPLICATION ENTRY POINT
# ===========================================================================

if __name__ == "__main__":
    with app.app_context():
        # Automatically create all database tables on first run
        db.create_all()
        ensure_reaction_columns()
        ensure_upload_folders()
        # Seed predefined categories if they don't exist yet
        for cat_name in PREDEFINED_CATEGORIES:
            if not Category.query.filter_by(name=cat_name).first():
                db.session.add(Category(name=cat_name))
        db.session.commit()
    app.run(debug=True)
