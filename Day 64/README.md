# Day 64 — Top 10 Movies Website (Flask + SQLAlchemy + TMDB API)

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: My Top 10 Movies

A Flask website that lets you search for a movie using **The Movie Database (TMDB) API**, add it to your personal ranked list, rate/review it, and see all movies auto-ranked from best to worst. Data is stored in a real database (SQLite) using **Flask-SQLAlchemy**, not a CSV file anymore.

---

## 🧠 Concepts Covered

### 1. Flask-SQLAlchemy: defining a database model
Instead of manually writing SQL, `Flask-SQLAlchemy` lets you define a table as a Python class. Each attribute becomes a column.

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
```
This is the modern (2.0-style) SQLAlchemy syntax using type-annotated `Mapped[]` columns instead of the older `db.Column(db.Integer)` style.

### 2. Creating the database and tables automatically
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db.init_app(app)

with app.app_context():
    db.create_all()
```
`db.create_all()` only creates tables that don't already exist — it won't overwrite existing data. The `.db` file is auto-created inside an `instance/` folder.

### 3. Calling an external API (TMDB) with `requests`
When the user searches for a movie title, the app queries TMDB's search endpoint and returns a list of matching results for the user to pick from.

```python
import requests

MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"

response = requests.get(MOVIE_DB_SEARCH_URL, params={
    "api_key": MOVIE_DB_API_KEY,
    "query": movie_title
})
data = response.json()["results"]
```
Passing `params={...}` lets `requests` handle URL-encoding the query string automatically instead of building it by hand.

### 4. A two-step "search then confirm" flow
Rather than adding a movie the moment the title is typed, the app shows a **selection page** first (`/add` → `select.html`), since a title search can return multiple matches (e.g. remakes, sequels). The user clicks the correct one, which passes its TMDB `id` to `/find`.

```python
@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    response = requests.get(f"{MOVIE_DB_INFO_URL}/{movie_api_id}",
                             params={"api_key": MOVIE_DB_API_KEY})
    data = response.json()
    new_movie = Movie(
        title=data["title"],
        year=data["release_date"].split("-")[0],
        img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
        description=data["overview"]
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for("rate_movie", id=new_movie.id))
```
This immediately redirects to the rating form, so the movie is added *and* the user is prompted to rate it in one flow.

### 5. Auto-ranking movies by rating
On the home page, all movies are pulled from the DB sorted by rating, then a loop assigns ranking numbers — the highest-rated movie gets rank 1.

```python
result = db.session.execute(db.select(Movie).order_by(Movie.rating))
all_movies = result.scalars().all()

for i in range(len(all_movies)):
    all_movies[i].ranking = len(all_movies) - i
db.session.commit()
```
This re-calculates rankings on *every* page load, so the list always reflects the current data — no manual re-ordering needed.

### 6. Editing and deleting records
```python
@app.route("/delete")
def delete_movie():
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))
```
`db.get_or_404()` automatically returns a proper 404 error page if someone passes an invalid/non-existent ID, instead of crashing the app.

---

## 📂 Project Structure
```
day64/
├── main.py
├── requirements.txt
├── instance/
│   └── movies.db          # auto-created SQLite database
├── static/
│   └── css/styles.css
└── templates/
    ├── base.html
    ├── index.html
    ├── add.html
    ├── select.html
    └── edit.html
```

## 🔑 Before You Run: Get a TMDB API Key
This project needs a free API key from **The Movie Database**:
1. Create an account at https://www.themoviedb.org/
2. Go to Settings → API → request a free API key (Developer)
3. In `main.py`, replace:
   ```python
   MOVIE_DB_API_KEY = "USE_YOUR_OWN_CODE"
   ```
   with your actual key.

## ▶️ How to Run
```bash
pip install -r requirements.txt
python main.py
```
Visit `http://127.0.0.1:5000/` — click **Add Movie**, search a title, pick the right result, then rate/review it.

⚠️ **Note:** An `instance/movies.db` file is already included in this project with sample data. If you want a fresh start, delete that file before running — Flask-SQLAlchemy will create a new empty one automatically.

---

## 🖼️ Output
<img width="1341" height="637" alt="image" src="https://github.com/user-attachments/assets/b287d9c8-aa26-4b36-b18a-b45e0adb4f11" />
<img width="1366" height="524" alt="image" src="https://github.com/user-attachments/assets/e6baeee0-2aa1-48c7-8027-2afca76183d1" />
<img width="1346" height="634" alt="image" src="https://github.com/user-attachments/assets/32e852fe-9348-4ed8-9937-5884b900c277" />
<img width="1364" height="616" alt="image" src="https://github.com/user-attachments/assets/c6b21a2d-a74d-464f-bd3e-ba1d9c9f8adb" />
<img width="1356" height="630" alt="image" src="https://github.com/user-attachments/assets/bef51dea-1e13-43bc-8769-23c85de7aadb" />

<img width="1350" height="635" alt="image" src="https://github.com/user-attachments/assets/150ed2ce-5213-4fb9-bb43-92198205fd63" />

---

## ✅ Key Takeaways
- Flask-SQLAlchemy models replace raw SQL with Python classes — cleaner and safer against SQL injection.
- `db.create_all()` is safe to call every run — it never overwrites existing tables.
- External APIs (like TMDB) are called with `requests.get(url, params={...})` — always keep API keys out of version control in real projects (use `.env` files).
- A "search → select → confirm" flow is a common, user-friendly pattern when an API can return multiple ambiguous matches.
- Recalculating `ranking` on every home-page load keeps the list always accurate without needing a manual "sort" action.

## 📝 Practice Tasks
1. Move `MOVIE_DB_API_KEY` out of `main.py` into a `.env` file using `python-dotenv`.
2. Add a search-results "no matches found" message when TMDB returns an empty list.
3. Limit the list to the top 10 movies only (hide/delete beyond rank 10).
4. Add a confirmation step before deleting a movie (currently it deletes instantly on click).
