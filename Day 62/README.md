# Day 62 — Building Advanced Forms with Flask-WTF ☕

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey.

## 📌 Project: Cafe & Wifi

A Flask web app where users can browse a list of cafes and add new ones through a proper HTML form — built with **Flask-WTF** instead of raw HTML forms. New cafe entries are validated, then appended to a CSV file that acts as a simple database.

---

## 🧠 Concepts Covered

### 1. Why Flask-WTF instead of plain HTML forms
Plain HTML forms need manual validation, manual CSRF protection, and manual re-rendering of error messages. `Flask-WTF` wraps `WTForms` and gives you:
- Built-in **CSRF protection** (a hidden token added automatically)
- Server-side **validation** with reusable validator classes
- Python classes that describe the form, so the form and the validation logic live in one place

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    submit = SubmitField('Submit')
```

### 2. Advanced field types
Beyond basic `StringField`, WTForms ships purpose-built fields:

- **`URLField`** — renders an `<input type="url">` and validates the format
- **`SelectField`** — renders a `<select>` dropdown from a list of choices

```python
from wtforms import URLField, SelectField
from wtforms.validators import URL

location = URLField('Cafe Location (Google Maps URL)',
                     validators=[DataRequired(), URL()])

coffee_rating = SelectField('Coffee Rating',
                             choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'])
```
Using the *right* field type means the browser gives users a better input experience (e.g. a dropdown instead of free text) and WTForms validates the format automatically.

### 3. Custom validators
`URL()` checks that whatever the user types actually looks like a URL, and rejects the form with an error message if it doesn't.

```python
from wtforms.validators import URL
location = URLField('Location', validators=[
    DataRequired(),
    URL(message="Please enter a valid URL.")
])
```

### 4. CSRF protection (automatic)
Flask-WTF automatically injects a hidden CSRF token into every form and validates it on submit — this is what `app.config['SECRET_KEY']` is used for. Without a secret key, `FlaskForm` will refuse to work.

```python
app.config['SECRET_KEY'] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
```
⚠️ In a real production app, this should come from an environment variable, not be hardcoded.

### 5. Rendering forms quickly with Bootstrap-Flask
Instead of writing out every `<label>` and `<input>` by hand in the template, `Bootstrap-Flask`'s `render_form()` macro renders the whole form — labels, inputs, error messages, and styling — in one line.

```jinja2
{% from 'bootstrap5/form.html' import render_form %}
{{ render_form(form, novalidate=True, button_style="primary") }}
```

### 6. Handling submitted data in the route
`form.validate_on_submit()` does two things in one call: checks it's a POST request, AND runs all validators. Only if both pass does the code inside the `if` run.

```python
@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        # form.cafe.data, form.location.data, etc. are now available
        ...
        return redirect(url_for('home'))
    return render_template('add.html', form=form)
```

### 7. Writing validated data to CSV
Once the form passes validation, the data is appended as a new row using Python's built-in `csv` module.

```python
import csv
with open("cafe-data.csv", mode="a", newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([form.cafe.data, form.location.data, ...])
```

---

## 📂 Project Structure
```
day61/
├── main.py
├── forms.py
├── requirements.txt
├── cafe-data.csv          # auto-created on first submission
├── templates/
│   ├── base.html
│   ├── add.html
│   └── cafes.html
└── screenshots/
    └── day61_output.png
```

## ▶️ How to Run
```bash
pip install -r requirements.txt
python main.py
```
Visit `http://127.0.0.1:5000/` to see the cafe list, and `/add` to add a new one.

---

## 🖼️ Output
<img width="1366" height="571" alt="image" src="https://github.com/user-attachments/assets/1558096a-c027-4e75-9d25-02d74f6d15bb" />

---

## ✅ Key Takeaways
- Flask-WTF turns forms into Python classes — validation logic lives with the field, not scattered across the template.
- Use the **right field type** (`URLField`, `SelectField`) instead of forcing everything into `StringField`.
- `SECRET_KEY` is required for CSRF protection to work — never skip it, never hardcode it in real projects.
- `form.validate_on_submit()` combines the POST check and validation into one clean condition.
- Bootstrap-Flask's `render_form()` saves a lot of repetitive HTML while keeping forms accessible and styled.

## 📝 Practice Tasks
1. Add a `RadioField` for "Has WiFi? Yes/No" instead of a text-based rating.
2. Add server-side validation that rejects a cafe name shorter than 3 characters.
3. Add a delete route that removes a row from the CSV by cafe name.
4. Switch storage from CSV to SQLite using Flask-SQLAlchemy (preview of later days).
