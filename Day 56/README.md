
# Day 56 — Static Files, HTML, CSS, Rendering & Personal Site

## 📚 Course

**Python Development Pro Bootcamp**

## 📅 Day

**Day 56**

---

## 📌 Topics Covered

* Static Files
* HTML Files
* CSS Files
* Flask Static Folder
* Rendering HTML
* Jinja Templates
* Flask Web Development
* Linking CSS with HTML
* Personal Website
* Website Structure
* Frontend & Backend Integration

---

## 🌐 Day 56 Overview

On Day 56, I continued learning **web development with Flask** and focused on working with static files such as **HTML and CSS**.

I learned how Flask separates dynamic templates from static resources and how HTML and CSS can be combined to create a properly designed website.

As a practical project, I built a **Personal Site** using Flask, HTML, and CSS.

---

## 🖥️ 1. HTML

HTML (**HyperText Markup Language**) is used to create the structure of a web page.

I practiced creating elements such as:

* Headings
* Paragraphs
* Links
* Images
* Sections
* Navigation
* Buttons

Example:

```html
<h1>Welcome to My Website</h1>
<p>This is my personal website.</p>
```

---

## 🎨 2. CSS

CSS (**Cascading Style Sheets**) is used to control the appearance and layout of a website.

I practiced styling:

* Colors
* Fonts
* Spacing
* Backgrounds
* Buttons
* Layouts
* Images
* Navigation bars

Example:

```css
body {
    font-family: Arial, sans-serif;
    text-align: center;
}
```

---

## 📁 3. Static Files in Flask

Flask uses a special folder called:

```text
static/
```

for files that don't need to be dynamically generated.

Examples include:

```text
static/
├── css/
│   └── style.css
├── images/
│   └── profile.png
└── js/
    └── script.js
```

These files can be used by the HTML templates.

---

## 🧩 4. Flask Templates

HTML pages are stored inside the:

```text
templates/
```

folder.

Example project structure:

```text
Day 56/
│
├── main.py
│
├── templates/
│   └── index.html
│
└── static/
    └── css/
        └── style.css
```

Flask can render the HTML using:

```python
from flask import render_template

@app.route("/")
def home():
    return render_template("index.html")
```

---

## 🔗 5. Connecting CSS with Flask

The CSS file can be linked to an HTML template using Flask's `url_for()` function:

```html
<link
    rel="stylesheet"
    href="{{ url_for('static', filename='css/style.css') }}"
>
```

This tells Flask to load the CSS file from the `static` folder.

---

## 👩‍💻 6. Personal Site Project

The main practical project of Day 56 was creating a **Personal Site**.

The website provides a place to introduce myself, showcase my skills, and present information about my development journey.

### Website Sections

The personal site can include:

* Home
* About Me
* Skills
* Projects
* Contact
* Social Media Links

---

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **HTML5**
* **CSS3**
* **Jinja2**
* **Static Files**
* **Web Development**

---

## 🧠 What I Learned

Through Day 56, I learned:

* How Flask handles static files
* How to organize HTML and CSS files
* How Flask renders HTML templates
* How to use Jinja templates
* How to connect CSS with Flask
* How to structure a Flask project
* How frontend and backend work together
* How to create a personal website

---

## 🚀 Key Takeaway

**Day 56 was another important step toward becoming a full-stack developer.**

I learned how to combine **Flask, HTML, CSS, templates, and static files** to build a complete personal website instead of working with plain Python output.

Building a personal site also helped me understand how the concepts learned in previous Flask lessons can be combined into a real web project. 💻🌐

---

## 📈 Progress

**Python Development Pro Bootcamp — Day 56/100**

Continuing my journey of learning Python and web development by building practical projects and improving my frontend and backend skills. 🚀

---
## Screenshoot

<img width="1186" height="636" alt="image" src="https://github.com/user-attachments/assets/091d27d2-f6e0-453c-aa63-83e8b276d8ad" />


## 🔖 Topics

`Python` `Flask` `HTML` `CSS` `Static Files` `Jinja2` `Rendering` `Web Development` `Personal Website` `Frontend` `Backend`
