# Day 59 — Blog Capstone Project: Styling

## 📚 Course

**Python Development Pro Bootcamp**

---

## 📌 Topics Covered

* Flask Web Development
* Blog Website
* HTML
* CSS
* Bootstrap
* Jinja2
* Template Inheritance
* Static Files
* Responsive Web Design
* Website Styling
* Navigation Bar
* Blog Cards
* Forms
* Buttons
* Layout & Typography
* Frontend Integration

---

## 📝 Day 59 Overview

On Day 59, I worked on the **Blog Capstone Project** and focused on improving the visual design and styling of the blog application.

The main goal was to transform a basic Flask blog into a more polished, responsive, and user-friendly web application using **HTML, CSS, Bootstrap, Jinja2, and Flask**.

This project allowed me to combine the web-development concepts I learned during the previous days into one practical application.

---

## 🚀 Blog Capstone Project

The Blog Capstone Project is a web application where users can view blog posts through a structured and styled interface.

The project includes a frontend built with HTML, CSS, and Bootstrap while Flask and Jinja2 handle the backend and dynamic content rendering.

---

## 🎯 Project Objectives

The main objectives were to:

* Create a professional-looking blog interface
* Style blog posts using CSS and Bootstrap
* Create a responsive layout
* Use reusable Jinja templates
* Organize static CSS files
* Improve navigation and user experience
* Display blog content dynamically
* Connect frontend design with Flask

---

## 🎨 Styling

The major focus of Day 59 was **styling the blog application**.

I worked on:

* Page layouts
* Typography
* Colors
* Spacing
* Buttons
* Navigation
* Blog cards
* Headers
* Footers
* Forms
* Responsive layouts

CSS was used to customize the appearance while Bootstrap helped create responsive components more efficiently.

---

## 🧩 Bootstrap Integration

Bootstrap was used to make the blog responsive and improve the UI.

I practiced using:

* Bootstrap containers
* Rows and columns
* Navigation bars
* Buttons
* Cards
* Forms
* Responsive utilities
* Spacing classes

Example:

```html id="q0f9lm"
<div class="container">

    <div class="row">

        <div class="col-lg-8">
            Blog Content
        </div>

        <div class="col-lg-4">
            Sidebar
        </div>

    </div>

</div>
```

---

## 🧱 Jinja Template Inheritance

I used Jinja's template inheritance to avoid repeating common HTML code.

A base template can contain:

* Navbar
* Footer
* CSS links
* Common page structure

Other pages can extend the base template:

```html id="g5k8rb"
{% extends "base.html" %}

{% block content %}

<h1>My Blog</h1>

{% endblock %}
```

This makes the project more organized and maintainable.

---

## 📁 Static Files

CSS and other static resources were organized inside the `static` directory.

Example:

```text id="m9b3qa"
static/
│
├── css/
│   └── styles.css
│
└── images/
```

Flask can load the CSS file using:

```html id="x7c2pn"
<link
    rel="stylesheet"
    href="{{ url_for('static', filename='css/styles.css') }}"
>
```

---

## 📱 Responsive Design

The blog was designed to work across different screen sizes.

The layout can adapt to:

* 💻 Desktop
* 💻 Laptop
* 📱 Mobile
* 📲 Tablet

Bootstrap's responsive grid and CSS media queries helped achieve this.

---

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **HTML5**
* **CSS3**
* **Bootstrap**
* **Jinja2**
* **Responsive Web Design**

---

## 📂 Project Structure

```text id="w8q6cd"
Day 59/
│
├── main.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── post.html
│   ├── about.html
│   └── contact.html
│
└── static/
    ├── css/
    │   └── styles.css
    │
    └── images/
```

---

## 🧠 What I Learned

Day 59 helped me understand how frontend design can be integrated into a Flask application.

I learned:

* How to style Flask applications
* How to organize CSS files
* How to use Bootstrap for responsive design
* How Jinja template inheritance works
* How to create reusable layouts
* How to design blog cards and sections
* How to create responsive pages
* How frontend and backend work together
* How to improve the overall user experience

---

## 🏆 Key Takeaway

**Day 59 was an important milestone in my web-development journey.**

I combined Flask, Jinja2, HTML, CSS, and Bootstrap to transform a basic blog application into a more polished and responsive web project.

This project strengthened both my **frontend styling skills and Flask development skills**. 💻🌐

---

## 📈 Progress

**Python Development Pro Bootcamp — Day 59/100**

Continuing my journey of learning Python and full-stack web development by building practical applications and improving my frontend and backend skills. 🚀

---
## Screenshoot

<img width="1353" height="644" alt="image" src="https://github.com/user-attachments/assets/dafc5695-f41b-40c8-84e4-95e9d064144a" />
<img width="1346" height="618" alt="image" src="https://github.com/user-attachments/assets/eb8f46a0-c824-4876-b9fe-7ec6cca62659" />
<img width="1337" height="633" alt="image" src="https://github.com/user-attachments/assets/680a028e-f768-4dbc-92d4-29b9284683a1" />

## 🔖 Topics

`Python` `Flask` `Blog Capstone` `HTML` `CSS` `Bootstrap` `Jinja2` `Template Inheritance` `Static Files` `Responsive Design` `Web Development` `Frontend Development`
