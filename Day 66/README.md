# Day 66 — Building Your Own API with RESTful Routing

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: Cafe & Wifi REST API

A pure backend Flask API (no user-facing forms) for managing cafe data — supporting full **CRUD** operations (Create, Read, Update, Delete) using proper HTTP methods and returning JSON responses, following REST conventions.

Unlike Day 61/64 (which render HTML pages), this project has **no frontend forms** — all data is sent/received as JSON or form data via HTTP requests (e.g. through Postman or `curl`), exactly how real-world APIs work.

---

## 🧠 Concepts Covered

### 1. What makes an API "RESTful"
REST (Representational State Transfer) is a convention where each HTTP method maps to an action:
- **GET** → read data
- **POST** → create new data
- **PATCH** → partially update existing data
- **DELETE** → remove data

```python
@app.route("/add", methods=["POST"])
def add_cafe():
    ...

@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_new_price(cafe_id):
    ...

@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    ...
```
This is different from Day 64's app, where every route (including "delete") used a plain `GET` link — REST convention says destructive actions like delete should never be a simple `GET` (a bot/crawler following links could accidentally trigger it).

### 2. Returning JSON with `jsonify()`
Flask's `jsonify()` converts a Python dictionary into a proper JSON HTTP response, and sets the correct `Content-Type: application/json` header automatically.

```python
from flask import jsonify

@app.route("/random")
def get_random_cafe():
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())
```

### 3. Converting a database model to a dictionary
Instead of manually typing out every field name, looping through `self.__table__.columns` automatically builds a dictionary from *any* model — even if columns are added later.

```python
def to_dict(self):
    return {column.name: getattr(self, column.name) for column in self.__table__.columns}
```

### 4. Reading query parameters
`request.args.get()` reads values passed in the URL after a `?`, e.g. `/search?loc=London`.

```python
@app.route("/search")
def search_cafe():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
```

### 5. Proper HTTP status codes
A REST API should return meaningful status codes, not just `200` for everything:
- `200 OK` — success
- `403 Forbidden` — no/incorrect permission (wrong API key)
- `404 Not Found` — resource doesn't exist

```python
if all_cafes:
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
else:
    return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404
```

### 6. Protecting destructive routes with an API key
The `DELETE` route requires a matching `api-key` query parameter before it will delete anything — a basic form of authentication.

```python
API_KEY = "TopSecretAPIKey"

@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == API_KEY:
        ...
    else:
        return jsonify(error={"Forbidden": "..."}), 403
```
⚠️ This hardcoded key is fine for learning, but in a real app it should be stored in an environment variable and use a proper auth system (e.g. tokens, OAuth).

### 7. `db.get_or_404()` for safe lookups
Automatically returns a proper 404 response if a record with that ID doesn't exist, instead of the app crashing.

```python
cafe = db.get_or_404(Cafe, cafe_id)
```

---

## 📂 Project Structure
```
day66/
├── main.py
├── requirements.txt
├── templates/
│   └── index.html      # simple API docs page
└── cafes.db             # auto-created on first run (empty)
```

## ▶️ How to Run
```bash
pip install -r requirements.txt
python main.py
```
Visit `http://127.0.0.1:5000/` for a simple docs page listing all endpoints.

## 🧪 How to Test the Endpoints
Since this is a pure API (no forms), test it with a tool like **Postman**, **Thunder Client** (VS Code extension), or `curl`:

```bash
# Get a random cafe
curl http://127.0.0.1:5000/random

# Get all cafes
curl http://127.0.0.1:5000/all

# Search by location
curl "http://127.0.0.1:5000/search?loc=London"

# Add a new cafe (form data)
curl -X POST http://127.0.0.1:5000/add \
  -d "name=New Cafe&map_url=https://maps.com&img_url=https://img.com&loc=London&sockets=1&toilet=1&wifi=1&calls=0&seats=10-20&coffee_price=£2.50"

# Update coffee price
curl -X PATCH "http://127.0.0.1:5000/update-price/1?new_price=£3.00"

# Delete a cafe (requires API key)
curl -X DELETE "http://127.0.0.1:5000/report-closed/1?api-key=TopSecretAPIKey"
```

All 6 endpoints were tested locally with Flask's test client before this README was written — all returned expected status codes (200 / 403 / 404).

---

## 🖼️ Output

<img width="1362" height="628" alt="image" src="https://github.com/user-attachments/assets/922f74f1-641f-4de4-a38f-194851c8c09a" />
---
## ✅ Key Takeaways
- REST convention: `GET` = read, `POST` = create, `PATCH` = update, `DELETE` = remove — matching the HTTP method to the action, not just using GET for everything.
- Destructive actions (delete) should **never** be a plain `GET` link — use `DELETE` and protect it.
- `jsonify()` + a `to_dict()` helper method makes returning clean JSON from SQLAlchemy models painless.
- Return proper HTTP status codes (`404`, `403`) instead of always returning `200` — this is what makes an API predictable for other developers to consume.
- A hardcoded API key is fine for learning REST concepts, but real APIs need proper secret management and authentication.

## 📝 Practice Tasks
1. Add a `GET /cafe/<id>` route that returns a single cafe by ID (currently only `/all`, `/random`, `/search` exist).
2. Move `API_KEY` into an environment variable using `python-dotenv`.
3. Add a `PUT` route that fully replaces a cafe's data (vs `PATCH` which only updates the price).
4. Add basic input validation on `/add` — reject the request with a `400` status if `name` or `loc` is missing.
