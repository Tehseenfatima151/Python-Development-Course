# Day 68 — Authentication with Flask

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: User Registration & Login System

Adding proper user authentication to a Flask app — registration, login, logout, and protecting certain pages so only logged-in users can access them. Uses **Flask-Login** for session management and **Werkzeug's security helpers** for password hashing (never storing plain-text passwords).

---

## 🧠 Concepts Covered

### 1. Never store plain-text passwords
Passwords must be **hashed** before saving to the database. A hash is a one-way transformation — even if the database is leaked, the real password can't be recovered directly.

```python
from werkzeug.security import generate_password_hash, check_password_hash

hashed_password = generate_password_hash(
    password,
    method='pbkdf2:sha256',
    salt_length=8
)
```
The `salt_length` adds random data to the hash so that even two users with the same password get completely different hashes.

### 2. Registering a new user
```python
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form.get('email'),
            name=request.form.get('name'),
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)  # log them in immediately after registering
        return redirect(url_for("secrets"))
    return render_template("register.html")
```

### 3. Checking for duplicate accounts
Before creating a new user, check whether that email already exists — otherwise the database's `unique=True` constraint on email would just crash the app.

```python
result = db.session.execute(db.select(User).where(User.email == request.form.get('email')))
user = result.scalar()
if user:
    flash("You've already signed up with that email, log in instead!")
    return redirect(url_for('login'))
```

### 4. Setting up Flask-Login
Flask-Login manages the "who is currently logged in" state using sessions/cookies, so you don't have to build that from scratch.

```python
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    # UserMixin adds is_authenticated, is_active, get_id() etc. automatically
    ...

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)
```
`user_loader` tells Flask-Login how to reload a user object from the ID stored in their session cookie on every request.

### 5. Logging a user in
```python
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if not user:
            flash("That email does not exist, please try again.")
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
        else:
            login_user(user)
            return redirect(url_for('secrets'))
    return render_template("login.html")
```
`check_password_hash()` re-hashes the entered password the same way and compares it to the stored hash — you never "un-hash" a password to compare it directly.

### 6. Protecting routes with `@login_required`
Any route decorated with `@login_required` automatically redirects unauthenticated visitors to the login page instead of showing the page.

```python
@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", name=current_user.name)
```
`current_user` is a special Flask-Login proxy that always refers to whoever is logged in for that request.

### 7. Logging out
```python
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
```
`logout_user()` clears the user's session data.

### 8. Flash messages for feedback
`flash()` stores a one-time message that survives a redirect, so users see *why* something failed (wrong password, duplicate email, etc.) instead of a silent failure.

```python
flash("Password incorrect, please try again.")
```
```jinja2
{% with messages = get_flashed_messages() %}
  {% if messages %}
    {% for message in messages %}
      <p class="alert">{{ message }}</p>
    {% endfor %}
  {% endif %}
{% endwith %}
```

---

## 📂 Typical Project Structure
```
day68/
├── main.py
├── requirements.txt
├── static/
│   └── css/styles.css
└── templates/
    ├── index.html
    ├── register.html
    ├── login.html
    └── secrets.html      # protected page, only visible when logged in
```

## ▶️ How to Run
```bash
pip install -r requirements.txt
python main.py
```
Visit `http://127.0.0.1:5000/` → register a new account → get redirected to the protected `/secrets` page → try `/logout`, then try visiting `/secrets` again to confirm it redirects you to login.

---

## 🖼️ Output
<img width="1342" height="637" alt="image" src="https://github.com/user-attachments/assets/34cf17f8-5606-4e53-832f-e2d143e56e24" />

---

## ✅ Key Takeaways
- Never store plain-text passwords — always hash with `generate_password_hash()`, and never try to reverse a hash to "check" a password.
- `check_password_hash()` compares hashes, it doesn't decrypt anything — hashing is one-way by design.
- Flask-Login's `UserMixin` + `user_loader` handles session/cookie logic so you don't reinvent authentication from scratch.
- `@login_required` is the simplest way to protect a route — no manual "if not logged in, redirect" checks needed on every view.
- `flash()` messages give users clear feedback (wrong password, duplicate email) instead of a confusing silent failure.
- `current_user` is available anywhere in a request once Flask-Login is set up — no need to pass the user manually to every template.

## 📝 Practice Tasks
1. Add a minimum password length check before hashing (e.g. reject anything under 8 characters).
2. Add a "Remember Me" checkbox on login using Flask-Login's `login_user(user, remember=True)`.
3. Show/hide the Register vs Login vs Logout nav links based on `current_user.is_authenticated`.
4. Add a custom error message when someone tries to access `/secrets` while logged out, instead of the default Flask-Login redirect.
