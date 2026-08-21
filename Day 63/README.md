# Day 63 — Website with SQLite Database using SQLAlchemy 📚

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: My Library

A Flask web app to manage a personal book library — add books, view them all, update their rating, or delete them. This is my first project using a **real database (SQLite)** instead of a CSV file, connected through **Flask-SQLAlchemy** (an ORM).

---

## 🧠 Concepts Covered

### 1. What is an ORM, and why use one?
Instead of writing raw SQL (`INSERT INTO books VALUES (...)`), an **ORM (Object-Relational Mapper)** lets you work with Python classes and objects, and it translates that into SQL behind the scenes.

```python
new_book = Book(title="Atomic Habits", author="James Clear", rating=9.5)
db.session.add(new_book)
db.session.commit()
```
This is safer (no SQL injection risk from string-building) and easier to read than raw SQL queries.

### 2. Setting up Flask-SQLAlchemy
Three steps connect Flask to a database:

```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)
```
- `SQLALCHEMY_DATABASE_URI` tells Flask *where* the database lives (here, a local SQLite file).
- `db.init_app(app)` binds the SQLAlchemy extension to this specific Flask app.

### 3. Defining a table as a Python class
Each table becomes a class, and each column becomes a `mapped_column`. This is the **new SQLAlchemy 2.0 typed syntax** (older tutorials use `db.Column` instead — both work, but this is the modern approach).

```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
```
- `primary_key=True` → unique identifier for each row.
- `unique=True` → no two books can have the exact same title.
- `nullable=False` → this field can't be left empty.

### 4. Creating the actual database file
Defining the class only describes the *schema* — this line actually creates `books.db` (if it doesn't already exist) with the matching table:

```python
with app.app_context():
    db.create_all()
```
This must run inside `app.app_context()` because SQLAlchemy needs to know which Flask app it's attached to.

### 5. CREATE — Adding a new record
```python
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")
```
`db.session.add()` stages the new row; `db.session.commit()` actually saves it to the database file.

### 6. READ — Querying all records
```python
result = db.session.execute(db.select(Book).order_by(Book.title))
all_books = result.scalars()
```
- `db.select(Book)` builds a SQL `SELECT * FROM books` query.
- `.order_by(Book.title)` sorts results alphabetically.
- `.scalars()` unwraps the raw result rows into actual `Book` objects, so `book.title`, `book.author` etc. work directly in the template.

### 7. UPDATE — Editing a record by ID
```python
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = db.get_or_404(Book, book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)
    return render_template("edit_rating.html", book=book_selected)
```
`db.get_or_404()` fetches a row by its primary key, and automatically returns a 404 error page if no matching row exists — no manual `if book is None` check needed.

### 8. DELETE — Removing a record
```python
@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))
```
Same pattern: fetch by ID, then `db.session.delete()` + `db.session.commit()`.

---

## 📂 Project Structure
```
Day 63/
├── main.py
├── requirements.txt
├── instance/
│   └── books.db           # auto-created SQLite database
└── templates/
    ├── index.html
    ├── add.html
    └── edit_rating.html
```

## ▶️ How to Run
```bash
pip install -r requirements.txt
python main.py
```
Visit `http://127.0.0.1:5000/` — the book list starts empty until you add some via `/add`.

⚠️ **Important (fixed during setup):** the original `requirements.txt` pinned `SQLAlchemy==2.0.25`, which crashes on newer Python versions (3.13+/3.14) with a `TypingOnly` `AssertionError`. Fixed by upgrading:
```bash
pip install --upgrade sqlalchemy flask-sqlalchemy
```

---

## 🖼️ Output
<img width="1366" height="574" alt="image" src="https://github.com/user-attachments/assets/22900854-19db-4da2-adac-dcfdaec6014a" />

---

## ✅ Key Takeaways
- An ORM maps Python classes to database tables, so you write Python instead of raw SQL.
- `db.create_all()` only creates tables that don't already exist — it won't overwrite existing data.
- `db.get_or_404()` is a clean shortcut for "fetch this row, or show a 404 if it's missing."
- Always call `db.session.commit()` after `add()`/`delete()`/edits — without it, changes stay uncommitted and are lost.
- Pinned dependency versions (like `SQLAlchemy==2.0.25`) can break on newer Python versions — keep an eye on this when reusing old project templates.

## 📝 Practice Tasks
1. Add a "genre" column to the `Book` table and update the form to capture it.
2. Add sorting by rating (highest first) as an alternate view on the home page.
3. Add a confirmation step before deleting a book (currently it deletes immediately on click).
4. Try switching `SQLALCHEMY_DATABASE_URI` to a different SQLite filename and observe a fresh, empty database being created.
