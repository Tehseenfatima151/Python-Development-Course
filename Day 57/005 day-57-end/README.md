# Day 57 — URL Building & Templating with Jinja in Flask Apps

## 📚 Course

**Python Development Pro Bootcamp**

---

## 📌 Topics Covered

* URL Building in Flask
* `url_for()`
* Dynamic URLs
* Flask Routes
* Jinja Templating
* Jinja Expressions
* Jinja Variables
* Jinja Statements
* Template Inheritance
* Passing Data from Flask to HTML
* Dynamic Web Pages
* Flask Web Applications

---

## 🌐 Day 57 Overview

On Day 57, I continued learning **web development with Flask** and focused on **URL Building and Jinja Templating**.

I learned how Flask can dynamically generate URLs using `url_for()` and how Jinja can be used to create dynamic HTML templates.

These concepts make Flask applications more organized, reusable, and easier to maintain.

---

## 🔗 1. URL Building in Flask

Flask provides the `url_for()` function to generate URLs for different routes.

Instead of manually writing URLs, we can reference the Python function that handles the route.

Example:

```python id="l7gtg5"
from flask import Flask, url_for

app = Flask(__name__)


@app.route("/")
def home():
    return "Home Page"


@app.route("/about")
def about():
    return "About Page"
```

We can generate the URL for the `about()` function using:

```python id="l8b7yp"
url_for("about")
```

This produces:

```text id="p4v6ce"
/about
```

---

## 🎯 2. Why Use `url_for()`?

Using `url_for()` is better than hard-coding URLs because Flask automatically builds the correct URL.

For example:

```html id="x0q8kn"
<a href="{{ url_for('about') }}">About</a>
```

If the route changes later, the template does not need to be manually updated everywhere.

---

## 🧩 3. Dynamic URLs

Flask allows us to create dynamic routes.

Example:

```python id="v5b3y4"
@app.route("/user/<name>")
def user(name):
    return f"Hello {name}!"
```

The URL:

```text id="h0n7pd"
/user/Tehseen
```

will display:

```text id="3b6v7y"
Hello Tehseen!
```

Dynamic URLs are useful when building pages for different users, products, posts, or other resources.

---

## 🎨 4. Jinja Templating

**Jinja** is the templating engine commonly used with Flask.

It allows Python data to be inserted dynamically into HTML.

Example Flask code:

```python id="m9k1b2"
@app.route("/")
def home():
    return render_template(
        "index.html",
        name="Tehseen"
    )
```

Inside `index.html`:

```html id="2n9d1a"
<h1>Hello {{ name }}!</h1>
```

The browser will display:

```text id="4h7r9c"
Hello Tehseen!
```

---

## 📝 5. Jinja Variables

Variables are displayed using double curly brackets:

```html id="u6x1ae"
{{ variable }}
```

Example:

```html id="1f9j7h"
<h1>{{ name }}</h1>
<p>{{ description }}</p>
```

Flask passes the values to the template.

---

## 🔀 6. Jinja Statements

Jinja also allows logic inside HTML templates.

For example:

```html id="q4v7ms"
{% if logged_in %}
    <p>Welcome back!</p>
{% else %}
    <p>Please log in.</p>
{% endif %}
```

Jinja can also be used with loops:

```html id="g2r8pz"
<ul>

{% for item in items %}

    <li>{{ item }}</li>

{% endfor %}

</ul>
```

This allows dynamic content to be generated from Python data.

---

## 🏗️ 7. Template Inheritance

Jinja allows multiple HTML pages to share a common layout.

A base template can contain:

* Navigation
* Header
* Footer
* Common CSS
* Page structure

Example:

```text id="k3d9hx"
templates/
│
├── base.html
├── index.html
└── about.html
```

The child template can extend the base template:

```html id="8x2f1n"
{% extends "base.html" %}

{% block content %}

<h1>About Me</h1>

{% endblock %}
```

This prevents repeating the same HTML code across multiple pages.

---

## 🔄 8. Passing Data from Flask to Jinja

Flask can pass multiple values to a template.

Example:

```python id="c8r5wd"
@app.route("/")
def home():

    skills = [
        "Python",
        "Flask",
        "HTML",
        "CSS"
    ]

    return render_template(
        "index.html",
        name="Tehseen",
        skills=skills
    )
```

The Jinja template can display the list:

```html id="e7v2ka"
<h1>{{ name }}</h1>

<ul>

{% for skill in skills %}

    <li>{{ skill }}</li>

{% endfor %}

</ul>
```

---

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **Jinja2**
* **HTML**
* **URL Routing**
* **Dynamic Templates**

---

## 🧠 What I Learned

Day 57 helped me understand how Flask applications can become more dynamic and maintainable.

I learned:

* How to build URLs using `url_for()`
* How Flask handles dynamic routes
* How Jinja templates work
* How to display Python variables in HTML
* How to use conditions and loops in templates
* How to pass data from Flask to HTML
* How template inheritance reduces duplicate code
* How to create reusable web page layouts

---

## 🚀 Key Takeaway

**Day 57 strengthened my Flask and web-development skills.**

I learned how **URL building and Jinja templating** work together to create dynamic and reusable Flask applications.

Instead of creating separate static HTML pages, I can now use Python and Jinja to generate pages dynamically and efficiently. 💻🐍🌐

---

## 📈 Progress

**Python Development Pro Bootcamp — Day 57/100**

Continuing my journey of learning Python, Flask, backend development, and modern web application concepts. 🚀

---
## Screenshoot
<img width="881" height="512" alt="image" src="https://github.com/user-attachments/assets/269698ef-09bf-4c7e-b882-0867f046f1e2" />

## 🔖 Topics

`Python` `Flask` `Jinja2` `URL Building` `url_for` `Templating` `Dynamic URLs` `Template Inheritance` `Web Development` `Backend Development`
