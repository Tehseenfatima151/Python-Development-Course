# Day 55 — Advanced Decorators, HTML Parsing, HTML Rendering, URL Parsing & Class Debugging

## 📚 Course

**Python Development Pro Bootcamp**

---

## 📌 Topics Covered

* Advanced Python Decorators
* `*args` and `**kwargs`
* HTML Parsing
* HTML Rendering
* Flask Templates
* Jinja2
* URL Parsing
* URL Parameters
* Dynamic Routes
* Python Class Debugging
* Object-Oriented Programming Debugging
* Debugging Techniques

---

## 🎀 1. Advanced Python Decorators

On Day 55, I continued learning about **Python Decorators** and explored more advanced ways to use them.

Decorators allow us to modify the behavior of functions without changing their original implementation.

I practiced decorators that can work with functions accepting different arguments by using:

```python
*args
**kwargs
```

Example:

```python
def my_decorator(function):

    def wrapper(*args, **kwargs):
        print("Something is happening before the function.")
        result = function(*args, **kwargs)
        print("Something is happening after the function.")
        return result

    return wrapper
```

Decorators are commonly used for:

* Logging
* Authentication
* Validation
* Timing
* Access control
* Code reuse

---

## 🌐 2. HTML Parsing

I learned how HTML documents can be **parsed and analyzed using Python**.

HTML parsing allows a program to understand the structure of an HTML document and access specific elements.

For example:

```html
<h1>Hello World</h1>
<p>Welcome to my website.</p>
```

Python can parse this structure and extract useful information from it.

---

## 🖥️ 3. HTML Rendering

I learned how Flask can render HTML pages instead of returning plain text.

Using:

```python
from flask import render_template
```

we can render an HTML template:

```python
@app.route("/")
def home():
    return render_template("index.html")
```

Flask searches for HTML files inside the `templates` folder.

Project structure:

```text
project/
│
├── main.py
│
└── templates/
    └── index.html
```

---

## 🧩 4. Jinja Templates

I learned how **Jinja2** can be used to create dynamic HTML pages in Flask.

Python values can be passed into an HTML template:

```python
@app.route("/")
def home():
    return render_template(
        "index.html",
        name="Tehseen"
    )
```

Then the value can be displayed in HTML:

```html
<h1>Hello {{ name }}!</h1>
```

This allows the backend to dynamically generate web pages.

---

## 🔗 5. URL Parsing

I also learned how URLs are structured and how Flask can extract information from URLs.

For example:

```text
https://example.com/user/123
```

A dynamic Flask route can capture part of the URL:

```python
@app.route("/user/<username>")
def user(username):
    return f"Hello {username}!"
```

Visiting:

```text
/user/Tehseen
```

will produce:

```text
Hello Tehseen!
```

---

## 🛠️ 6. URL Parameters

URL parameters allow information to be passed through a URL.

Example:

```python
@app.route("/post/<int:post_id>")
def post(post_id):
    return f"Post ID: {post_id}"
```

The `<int:post_id>` part tells Flask that the value should be treated as an integer.

---

## 🐛 7. Class Debugging

Day 55 also focused on identifying and fixing errors inside Python classes.

When working with Object-Oriented Programming, bugs can occur because of:

* Incorrect attributes
* Incorrect method names
* Missing `self`
* Incorrect indentation
* Wrong object initialization
* Incorrect method calls
* Unexpected values

Example:

```python
class User:

    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello {self.name}"
```

Debugging helps identify where the program is behaving differently from what was expected.

---

## 🔍 Debugging Techniques

I practiced:

* Reading error messages
* Understanding tracebacks
* Using `print()` statements
* Checking variable values
* Checking function arguments
* Testing code step-by-step
* Finding logical errors
* Debugging class methods

---

## 🧠 What I Learned

Day 55 helped me move from basic Flask development toward more advanced Python web-development concepts.

I learned:

* How advanced decorators work
* How `*args` and `**kwargs` can be used in decorators
* How HTML can be parsed
* How Flask renders HTML templates
* How Jinja makes pages dynamic
* How URLs and URL parameters work
* How dynamic Flask routes are created
* How to debug Python classes
* How to read and understand Python errors

---

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **Jinja2**
* **HTML**
* **URL Routing**
* **Python Decorators**
* **Object-Oriented Programming**
* **Debugging**

---

## 🚀 Key Takeaway

**Day 55 strengthened my understanding of Python web development and debugging.**

I learned how decorators can make Python code more powerful and reusable, while Flask and Jinja allow Python to generate dynamic HTML pages.

I also improved my debugging skills by learning how to identify problems inside Python classes and understand error messages more effectively. 💻🐍

---

## 📈 Progress

**Python Development Pro Bootcamp — Day 55/100**

Continuing to build my Python, Flask, web development, and debugging skills through practical learning and projects. 🚀

---
## Screenshoot
<img width="898" height="590" alt="image" src="https://github.com/user-attachments/assets/94baf534-3872-4868-abdb-261e599c8631" />


## 🔖 Topics

`Python` `Advanced Decorators` `HTML Parsing` `HTML Rendering` `Flask` `Jinja2` `URL Parsing` `URL Routing` `OOP` `Class Debugging` `Debugging`
