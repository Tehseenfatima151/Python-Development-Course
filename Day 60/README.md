# Day 60 — POST Requests with Flask & HTML Forms

## 📚 Course

**Python Development Pro Bootcamp**

---

## 📌 Topics Covered

* HTTP Requests
* GET Requests
* POST Requests
* Flask
* HTML Forms
* Form Submission
* `request.form`
* Form Data Handling
* Flask Routes
* Jinja2
* `render_template()`
* Redirects
* Backend & Frontend Communication

---

## 🌐 Day 60 Overview

On Day 60, I learned how **HTML forms communicate with a Flask backend using POST requests**.

I learned how users can enter information into an HTML form and submit it to a Flask server, where Python can receive, process, and use the submitted data.

This was an important step toward understanding how interactive web applications work.

---

## 📤 1. GET vs POST Requests

### GET Request

A GET request is commonly used to **request or retrieve data** from a server.

Example:

```python id="w6t2q1"
@app.route("/about")
def about():
    return "About Page"
```

When a user visits `/about`, Flask receives a GET request.

---

### POST Request

A POST request is commonly used to **send data to a server**.

HTML forms often use POST when submitting information such as:

* Login details
* Contact forms
* Registration information
* Blog posts
* User feedback

---

## 📝 2. HTML Forms

An HTML form allows users to enter information.

Example:

```html id="g8p2xs"
<form action="/submit" method="POST">

    <input
        type="text"
        name="username"
        placeholder="Enter your name"
    >

    <input
        type="email"
        name="email"
        placeholder="Enter your email"
    >

    <button type="submit">
        Submit
    </button>

</form>
```

The important part is:

```html id="z6j4nt"
method="POST"
```

This tells the browser to send the form data using a POST request.

---

## 🐍 3. Handling POST Requests with Flask

Flask can receive POST requests by specifying the HTTP method in the route.

```python id="e3q8kc"
from flask import Flask, request

app = Flask(__name__)


@app.route("/submit", methods=["POST"])
def submit():

    username = request.form["username"]

    return f"Hello {username}!"
```

When the form is submitted, Flask receives the data.

---

## 📥 4. Using `request.form`

Flask provides:

```python id="j9k2wp"
request.form
```

to access submitted form data.

For example:

```python id="a3v7mn"
name = request.form["name"]
email = request.form["email"]
```

The values come from the HTML form's `name` attributes.

---

## 🔄 5. GET and POST in One Route

A route can handle both displaying a form and processing its submission.

Example:

```python id="r4x8yd"
@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]

        return f"Thanks, {name}!"

    return render_template("contact.html")
```

This allows the same route to:

1. Display the form using GET.
2. Process submitted data using POST.

---

## 🔗 6. Form Action

The `action` attribute determines where the form data is sent.

Example:

```html id="v8p3qm"
<form action="/contact" method="POST">
```

The form data will be sent to the `/contact` Flask route.

---

## 🧩 7. Jinja and Forms

Jinja can be used to dynamically display information after a form submission.

Example:

```python id="f2r7kn"
@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]

        return render_template(
            "success.html",
            name=name
        )

    return render_template("contact.html")
```

Then in `success.html`:

```html id="n6v9xa"
<h1>Thank you, {{ name }}!</h1>
```

---

## 🚀 Project Workflow

The basic workflow learned on Day 60 is:

```text id="z3k6wp"
User
  ↓
HTML Form
  ↓
Submit Button
  ↓
POST Request
  ↓
Flask Server
  ↓
request.form
  ↓
Process Data
  ↓
Response / HTML Page
```

---

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **HTML5**
* **Jinja2**
* **HTTP**
* **GET Requests**
* **POST Requests**
* **HTML Forms**

---

## 🧠 What I Learned

Day 60 helped me understand how frontend forms communicate with backend Python applications.

I learned:

* Difference between GET and POST
* How HTML forms work
* How to submit form data
* How Flask handles POST requests
* How to use `request.form`
* How to retrieve user input
* How to process submitted data
* How to use Jinja to display dynamic results
* How frontend and backend communicate

---

## 🏆 Key Takeaway

**Day 60 was an important step toward building interactive web applications.**

I learned how a user can enter information into an HTML form and send that information to a Flask backend using a **POST request**.

This concept is essential for building real-world features such as **contact forms, login systems, registration pages, feedback forms, and data submission systems**. 💻🐍🌐

---

## 📈 Progress

**Python Development Pro Bootcamp — Day 60/100**

Continuing my journey of learning Python, Flask, backend development, and full-stack web development through practical projects. 🚀

---
## Screenshoot
![Uploading image.png…]()

## 🔖 Topics

`Python` `Flask` `POST Request` `GET Request` `HTML Forms` `request.form` `Jinja2` `HTTP` `Backend Development` `Web Development`
