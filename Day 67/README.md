# Day 67 — Blog Capstone Project: Refactoring to RESTful Routing

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: RESTful Blog

This day takes the earlier Flask blog project (SQLite + Blog CRUD from CKEditor/WTForms days) and **refactors its routes to follow REST convention** — same features, but each route now uses the correct HTTP method for what it does, instead of everything being a `GET` request with different URLs.

---

## 🧠 Concepts Covered

### 1. Auditing existing routes against REST convention
Before refactoring, the first step is listing every existing route and checking whether its HTTP method matches its action:

| Action | Before (non-RESTful) | After (RESTful) |
|---|---|---|
| View all posts | `GET /` | `GET /` |
| View one post | `GET /post/<id>` | `GET /post/<id>` |
| Add a new post | `GET /new-post` (form) + `POST /new-post` (submit) | `GET /new-post` + `POST /new-post` *(already correct)* |
| Edit a post | `GET /edit-post/<id>` (form) + `POST /edit-post/<id>` (submit) | `GET /edit-post/<id>` + `PATCH /edit-post/<id>` |
| Delete a post | `GET /delete/<id>` ❌ | `DELETE /delete/<id>` ✅ |

The biggest red flag in most beginner blog projects is **delete-via-GET-link** — a simple `<a href="/delete/3">Delete</a>` link. Any crawler, browser prefetcher, or accidental click can trigger it. REST fixes this by requiring a `DELETE` request, which a plain link can never send on its own.

### 2. Why GET-based delete links are unsafe
```html
<!-- BEFORE: dangerous — GET is meant to be "safe" and side-effect-free -->
<a href="{{ url_for('delete_post', post_id=post.id) }}">Delete</a>
```
```python
# BEFORE
@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    ...
```
A `GET` request is supposed to only *retrieve* data, never change it. Search engine bots crawl every `GET` link they find — a bot could accidentally delete every post on the blog just by following links.

### 3. Sending non-GET/POST requests from HTML (the real-world limitation)
Plain HTML forms only support `GET` and `POST` — browsers can't natively submit `PATCH` or `DELETE`. Two common real solutions:
- **Small inline JavaScript using `fetch()`** to send the proper method
- **Method override**: a hidden `_method` field the backend reads and re-routes internally (common in some frameworks, less common in Flask)

```html
<!-- AFTER: uses JavaScript fetch to send an actual DELETE request -->
<button onclick="deletePost({{ post.id }})">Delete</button>

<script>
function deletePost(postId) {
    fetch(`/delete/${postId}`, { method: 'DELETE' })
        .then(() => window.location.reload());
}
</script>
```
```python
# AFTER
@app.route("/delete/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    ...
```

### 4. Separating "show the edit form" from "save the edit"
Non-RESTful blogs often reuse the same `GET`+`POST` pair for editing, which technically works but blurs the line between *reading* a form and *writing* a change. The RESTful pattern:
- `GET /edit-post/<id>` → returns the pre-filled form (read-only, safe)
- `PATCH /edit-post/<id>` → actually applies the change

```python
@app.route("/edit-post/<int:post_id>", methods=["GET", "PATCH"])
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(obj=post)
    if request.method == "PATCH" and edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)
```
*(Since HTML forms can't natively send PATCH, this route is triggered via `fetch()` from the edit page, same pattern as the delete button.)*

### 5. Consistent, predictable URL naming
REST also means URLs describe **resources**, not actions:
- ✅ `GET /posts/5` (the resource "post 5")
- ❌ `GET /view-blog-post-page?id=5` (an action-shaped URL)

Cleaning up inconsistent route names (`/new-post` vs `/add_new_post` vs `/createPost`) into one consistent style is part of this refactor.

---

## 📂 Typical Project Structure
```
day67/
├── main.py
├── requirements.txt
├── static/
│   └── css/styles.css
└── templates/
    ├── index.html
    ├── post.html
    ├── make-post.html      # shared by "new post" and "edit post"
    └── base.html
```

## ▶️ How to Run
```bash
pip install -r requirements.txt
python main.py
```
Visit `http://127.0.0.1:5000/` to view the blog, add/edit/delete posts using the refactored RESTful routes.

---

## 🖼️ Output
<img width="1342" height="637" alt="image" src="https://github.com/user-attachments/assets/a92bd926-fbe9-47fe-bf69-344c1d4f27ed" />

---

## ✅ Key Takeaways
- `GET` requests must never change data — delete/edit actions need `DELETE`/`PATCH`, not a clickable `GET` link.
- Plain HTML forms can only send `GET` or `POST` — real `DELETE`/`PATCH` requests from a browser require JavaScript's `fetch()`.
- Separate "show me the form" (`GET`, safe) from "apply the change" (`PATCH`/`POST`, has side effects) — don't conflate the two under one method.
- Consistent, resource-based URL naming (`/posts/<id>`) makes an API/site easier for other developers (and future-you) to understand.
- Refactoring an existing project to follow a convention is a normal, valuable step — code doesn't have to be "REST-perfect" on the first pass.

## 📝 Practice Tasks
1. Audit one of your earlier projects (e.g. the Cafe & Wifi Day 61 project) for any `GET`-based delete/edit links, and refactor them the same way.
2. Add a confirmation prompt (`confirm()` in JS) before the `fetch()` delete call actually fires.
3. Add a `PUT` route that fully replaces a blog post (title + body + author), separate from `PATCH` which could update just one field.
4. Write a short comment above each route explaining which REST action it represents — good habit for anyone reading your code later.
