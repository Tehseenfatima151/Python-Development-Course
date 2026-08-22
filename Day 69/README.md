
# Day 69 — Blog Capstone Project: Adding a User

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: Blog with User Accounts, Admin Rights & Comments

This day combines everything from Day 68 (authentication) with the earlier Blog Capstone (Day 58–59/67) — turning a single-admin blog into a **multi-user blog** where any registered user can comment, but only the original admin can create/edit/delete posts.

---

## 🧠 Concepts Covered

### 1. Linking database tables with a relationship (One-to-Many)
Instead of each `BlogPost` just having a plain `author` text field, it now has a proper **foreign key** pointing to a `User`. One user can write many posts — a classic one-to-many relationship.

```python
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

    # This "posts" is a virtual list — not an actual DB column
    posts: Mapped[list["BlogPost"]] = relationship(back_populates="author")


class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True)

    # Foreign Key — links this post to a row in the users table
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    # "author" refers to the User object, not a plain string anymore
    author: Mapped["User"] = relationship(back_populates="posts")
```
`back_populates` keeps both sides in sync — updating `post.author` also updates `user.posts` automatically, without extra queries.

### 2. A second relationship for Comments (also One-to-Many, twice over)
Comments have **two** foreign keys — one to the user who wrote it, one to the post it belongs to.

```python
class Comment(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="comments")

    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    parent_post: Mapped["BlogPost"] = relationship(back_populates="comments")
```
Each `Comment` "belongs to" exactly one `User` and exactly one `BlogPost` — but both `User` and `BlogPost` can have *many* comments pointing back to them.

### 3. Restricting actions to admin only, with a custom decorator
Rather than checking `if current_user.id == 1` inside every route, a reusable decorator wraps that logic once.

```python
from functools import wraps
from flask import abort

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    ...
```
`@wraps(f)` preserves the original function's name/metadata — without it, Flask can get confused when multiple routes are wrapped by the same decorator.

### 4. Adding comments as a logged-in user
```python
@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))

        new_comment = Comment(
            text=comment_form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("post.html", post=requested_post, form=comment_form)
```

### 5. Showing a Gravatar next to each comment
`Flask-Gravatar` auto-generates a profile picture for each commenter based on their email, without needing image upload/storage.

```python
from flask_gravatar import Gravatar

gravatar = Gravatar(app,
    size=100,
    rating='g',
    default='retro',
    force_default=False,
    force_lower=False,
    use_ssl=False,
    base_url=None)
```
```jinja2
<img src="{{ comment.comment_author.email | gravatar }}">
```

### 6. Conditionally showing admin controls in templates
The "Edit Post" / "Delete Post" buttons should only render for the admin — checked directly in Jinja using `current_user`.

```jinja2
{% if current_user.is_authenticated and current_user.id == 1 %}
  <a href="{{ url_for('edit_post', post_id=post.id) }}">Edit Post</a>
{% endif %}
```

---

## 📂 Typical Project Structure
```
day69/
├── main.py
├── requirements.txt
├── static/
│   └── css/styles.css
└── templates/
    ├── index.html
    ├── post.html          # shows post + comments + comment form
    ├── make-post.html
    ├── register.html
    ├── login.html
    └── base.html
```

## ▶️ How to Run
```bash
pip install -r requirements.txt
python main.py
```
Visit `http://127.0.0.1:5000/` → register a normal account (won't have admin rights) → try commenting on a post → log in as the first-ever registered user (id=1) to see the admin-only "New Post" / "Edit" / "Delete" controls.

---

## 🖼️ Output
![Uploading image.png…]()


---

## ✅ Key Takeaways
- `relationship()` + `ForeignKey` turn a plain text "author" field into a real link between tables — no duplicate/typo-prone data.
- `back_populates` keeps both sides of a relationship in sync automatically (e.g. `user.posts` and `post.author`).
- A custom `@admin_only` decorator avoids repeating the same permission check in every protected route.
- A `Comment` can have two foreign keys at once — one to the commenter, one to the post — modeling a proper many-to-one-to-many structure.
- Gravatar removes the need to build your own profile-picture upload system for a simple use case.
- Admin-only UI elements should be hidden in the template too (`{% if %}`), not just blocked at the route level — otherwise regular users see buttons that then 403 when clicked.

## 📝 Practice Tasks
1. Add a "Delete Comment" feature — admin can delete any comment, but a regular user can only delete their own.
2. Instead of hardcoding `current_user.id == 1` for admin, add an `is_admin` boolean column to the `User` model.
3. Show the total comment count on each post preview on the home page.
4. Add pagination so the home page only shows 5 posts at a time instead of all of them.
