# Day 54 — Command Line, Python Decorators & Web Development with Flask

## 📚 Course

**Python Development Pro Bootcamp**

---

## 📌 Topics Covered

* Command Line
* Terminal & Command Prompt
* Command Line Arguments
* Python Decorators
* Functions as First-Class Objects
* `*args` and `**kwargs`
* Higher-Order Functions
* Flask
* Web Development with Python
* Routes
* HTTP Methods
* HTML Templates
* Dynamic Web Pages
* Flask Development Server

---

## 🖥️ 1. Command Line

On Day 54, I learned how to work with the **Command Line** and interact with programs using the terminal.

Instead of always running Python programs through an IDE, I practiced running Python files directly from the terminal.

Example:

```bash
python main.py
```

I also learned how command-line arguments can be passed to Python programs.

---

## 🎀 2. Python Decorators

I learned about **Python Decorators**, which allow us to modify or extend the behavior of an existing function without changing its original code.

A basic decorator looks like:

```python
def my_decorator(function):

    def wrapper():
        print("Before the function")
        function()
        print("After the function")

    return wrapper
```

The decorator can then be applied using:

```python
@my_decorator
def say_hello():
    print("Hello!")
```

Decorators are useful for adding functionality such as:

* Logging
* Authentication
* Timing functions
* Access control
* Validation
* Code reuse

---

## 🌐 3. Web Development with Flask

I was introduced to **Flask**, a lightweight Python web framework used to build web applications and APIs.

Flask makes it possible to create web pages and handle requests using Python.

A basic Flask application:

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
```

When the application runs, Flask starts a development server that can be accessed through a web browser.

---

## 🛣️ 4. Flask Routes

I learned how Flask routes connect URLs to Python functions.

Example:

```python
@app.route("/about")
def about():
    return "About Page"
```

Now visiting `/about` calls the `about()` function.

Routes allow us to create different pages for a web application.

---

## 🧩 5. Dynamic Web Pages

Flask can also generate dynamic content.

For example:

```python
@app.route("/user/<name>")
def user(name):
    return f"Hello {name}!"
```

The value from the URL can be passed directly to the Python function.

---

## 📄 6. HTML Templates

Flask can render HTML pages using templates.

Example:

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")
```

Project structure:

```text
Day 54/
│
├── main.py
│
└── templates/
    └── index.html
```

This separates the Python backend from the HTML frontend.

---

## 🧠 What I Learned

Day 54 helped me understand how Python can be used beyond standalone programs.

I learned:

* How to use the command line
* How Python decorators work
* How functions can be passed around as objects
* How Flask creates web applications
* How routes work
* How to create dynamic URLs
* How to render HTML templates
* How Python can power the backend of a website

---

## 🛠️ Technologies Used

* **Python**
* **Command Line**
* **Flask**
* **HTML**
* **Jinja Templates**
* **Web Development**

---

## 📦 Installation

Install Flask using pip:

```bash
pip install flask
```

Or:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
Flask
```

---

## ▶️ How to Run

Open the project folder in VS Code and run:

```bash
python main.py
```

Flask will start the development server.

The terminal will provide the local URL where the application can be opened in a browser.

---

## 🚀 Key Takeaway

**Day 54 was an important step toward Python web development.**

I learned how command-line tools work, how decorators can extend function behavior, and how Flask can be used to build web applications using Python.

This day connected my Python fundamentals with **real-world backend and web development concepts**. 💻🐍🌐

---

## 📈 Progress

**Python Development Pro Bootcamp — Day 54/100**

Continuing my Python journey by learning web development and building a stronger foundation in backend programming. 🚀

---
## Screenshoot
<img width="1357" height="712" alt="image" src="https://github.com/user-attachments/assets/0702ec01-ccda-4a8b-ae26-2c1a8bcf2267" />

## 🔖 Topics

`Python` `Command Line` `Decorators` `Flask` `Web Development` `Backend Development` `Jinja` `HTML` `Python Web Framework`
