# 🤖 Day 49 – Automating Job Applications on LinkedIn

## 📌 Project Overview

Day 49 of the **Python Development Pro Bootcamp** focused on **Web Automation with Selenium**.

In this project, I built a Python automation bot that interacts with LinkedIn job listings and helps automate the job application process.

The project demonstrates how Selenium can be used to control a web browser, search for jobs, interact with web elements, and automate repetitive tasks.

---

## 🛠️ Technologies Used

* 🐍 Python
* 🌐 Selenium WebDriver
* 🌍 Google Chrome
* 🤖 Web Automation
* 💼 LinkedIn Jobs

---

## 💻 Project Features

* Automatically opens Google Chrome
* Opens LinkedIn Jobs
* Searches for relevant job listings
* Finds job cards using Selenium
* Opens job listings
* Interacts with application buttons
* Automates repetitive browser interactions
* Uses Selenium WebDriver for browser automation
* Handles web elements and page navigation

---

## 🧠 Concepts Learned

### Selenium WebDriver

Selenium allows Python programs to control a web browser automatically.

It can be used to:

* Open websites
* Find HTML elements
* Click buttons
* Enter text
* Read webpage content
* Navigate between pages
* Automate repetitive browser tasks

Example:

```python
from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://www.linkedin.com/jobs/")
```

---

## 🔎 Finding Web Elements

Selenium provides different methods for locating elements on a webpage.

For example:

```python
from selenium.webdriver.common.by import By

search_box = driver.find_element(
    By.CSS_SELECTOR,
    "input"
)
```

Selenium can then interact with the element:

```python
search_box.send_keys("Python Developer")
```

---

## 🖱️ Clicking Elements

Selenium can automatically click buttons and links.

Example:

```python
button = driver.find_element(
    By.CSS_SELECTOR,
    "button"
)

button.click()
```

---

## 🔄 Automation Workflow

The automation process follows this basic flow:

```text
Start
  ↓
Open Chrome
  ↓
Open LinkedIn Jobs
  ↓
Search for Jobs
  ↓
Find Job Listings
  ↓
Open Job
  ↓
Apply / Interact with Application
  ↓
Move to Next Job
  ↓
Continue
```

---

## 📂 Project Structure

```text
Day49/
│
├── main.py
├── requirements.txt
├── README.md
│
└── screenshots/
    └── day49_output.png
```

---

## 📦 Installation

Install Selenium using:

```bash
pip install selenium
```

Or install all dependencies:

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```text
selenium
```

---

## ▶️ How to Run

Open the project folder in VS Code.

Install the required dependency:

```bash
pip install selenium
```

Then run:

```bash
python main.py
```

The program will open Chrome and perform the configured LinkedIn job-search and automation tasks.

---
# Screenshoot
<img width="1366" height="585" alt="image" src="https://github.com/user-attachments/assets/6fbed4ee-e8a9-4fc7-974a-77bf6d427a1a" />

<img width="1366" height="581" alt="image" src="https://github.com/user-attachments/assets/af3e08a1-008b-4ed8-826c-0ba6e5f67590" />

<img width="1364" height="582" alt="image" src="https://github.com/user-attachments/assets/eade3eec-5eed-4d25-acae-b60c029509fa" />

<img width="1365" height="580" alt="image" src="https://github.com/user-attachments/assets/1bc7edae-aabb-4563-92da-468c81a8abde" />

<img width="1366" height="577" alt="image" src="https://github.com/user-attachments/assets/042c9b3d-32d4-43ae-a4b3-1a1598693db2" />

## ⚠️ Important Note

LinkedIn frequently changes its website structure and may require login, verification, CAPTCHA, or additional interaction.

Because of this, Selenium selectors may need to be updated when the LinkedIn website changes.

This project is primarily for **learning Selenium and browser automation**.

---

## 🎯 Learning Outcome

By completing this project, I learned how to:

* Use Selenium WebDriver
* Automate Google Chrome
* Locate web elements
* Interact with input fields and buttons
* Navigate dynamic websites
* Automate repetitive browser tasks
* Build practical web automation scripts

---

## 🚀 Skills Practiced

```text
Python
   ↓
Selenium
   ↓
WebDriver
   ↓
Browser Automation
   ↓
Web Element Interaction
   ↓
Job Search Automation
```

---

## 📚 Course

**Python Development Pro Bootcamp**

**Day 49 – Automating Job Applications on LinkedIn**

Another step forward in my Python automation journey! 🚀🐍
