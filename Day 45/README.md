# 📌 Day 45 — Intermediate CSS & Web Scraping with BeautifulSoup

## 🎯 Course

**Python Programming Pro Bootcamp**

---

## 📚 Topics Covered

On Day 45, I learned **Intermediate CSS** and started working with **Web Scraping using Python and BeautifulSoup**.

### 🎨 Intermediate CSS

I explored more advanced CSS concepts, including:

* CSS Selectors
* Specificity
* Positioning
* Display properties
* Flexbox
* Responsive design
* CSS Box Model
* Margins and Padding
* Borders
* Width and Height
* Styling HTML elements
* Combining HTML and CSS to create structured web pages

---

### 🕷️ Web Scraping with BeautifulSoup

I learned how to extract useful information from websites using Python.

#### Main concepts:

* Installing and importing `BeautifulSoup`
* Sending HTTP requests using `requests`
* Parsing HTML
* Finding HTML elements
* Using tags and attributes
* `find()`
* `find_all()`
* Extracting text with `.get_text()`
* Working with HTML structure
* Cleaning scraped data
* Saving scraped data into a file

Example:

```python
import requests
from bs4 import BeautifulSoup

response = requests.get("https://example.com")

soup = BeautifulSoup(response.text, "html.parser")

heading = soup.find("h1")

print(heading.get_text())
```

---

# 🎬 Project — 100 Movies You Must Watch

For the Day 45 project, I built a **Web Scraping project** that collects movie titles from a website and creates a list of **100 Movies You Must Watch**.

The project uses **BeautifulSoup** to scrape movie data from a web page.

### 🔎 Project Workflow

```text
Website
   ↓
Requests
   ↓
HTML Response
   ↓
BeautifulSoup
   ↓
Find Movie Titles
   ↓
Extract Text
   ↓
Reverse / Organize List
   ↓
Save Movies to File
```

---

## 🛠️ Technologies Used

* 🐍 Python
* 🌐 HTML
* 🎨 CSS
* 📦 Requests
* 🍲 BeautifulSoup
* 📄 Text File Handling

---

## 💻 Project Features

* Scrapes movie data from a website
* Uses BeautifulSoup to parse HTML
* Finds movie titles from HTML elements
* Extracts text from selected elements
* Organizes movie titles
* Creates a list of 100 movies
* Saves the final movie list into a text file

---

## 📂 Project Structure

```text
Day45/
│
├── main.py
├── movies.txt
└── README.md
```

---

## 🧠 What I Learned

Through this project, I learned how Python can interact with websites and extract useful information from HTML.

I practiced:

* Making HTTP requests
* Parsing HTML with BeautifulSoup
* Finding elements using tags and selectors
* Extracting text from HTML
* Working with scraped data
* Writing data to files
* Combining Python with web technologies

---

## 📸 Screenshot

<!-- Add your project screenshot here -->

<img width="1210" height="688" alt="image" src="https://github.com/user-attachments/assets/19fe4319-c3a1-403a-9a27-f72607ac39f5" />


---

## 🚀 Key Takeaway

Day 45 was an important step toward learning **Web Scraping and Automation with Python**.

I learned how to turn information available on a website into structured data that can be processed and stored using Python.

This project also gave me practical experience with **Requests, BeautifulSoup, HTML parsing, and file handling**.

---

## 📈 100 Days of Code

**Day 45 / 100** 🐍

Continuing my journey through the **Python Programming Pro Bootcamp** and building practical projects every day.

#Python #PythonProgramming #WebScraping #BeautifulSoup #WebDevelopment #CSS #100DaysOfCode #LearningInPublic
