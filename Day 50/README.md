# 💕 Day 50 – Tinder Swiping Bot

## 📌 Project Overview

Day 50 of the **Python Development Pro Bootcamp** focused on **Advanced Web Automation with Selenium**.

In this project, I built an automated Tinder swiping bot using Python and Selenium WebDriver.

The bot opens Tinder in a Chrome browser and automates repetitive swiping actions by interacting with buttons on the webpage.

This project helped me understand how Selenium can be used to automate real-world websites and browser interactions.

---

## 🛠️ Technologies Used

* 🐍 Python
* 🌐 Selenium WebDriver
* 🌍 Google Chrome
* 🤖 Web Automation
* 💕 Tinder

---

## 💻 Project Features

* Automatically opens Google Chrome
* Opens Tinder
* Handles browser interactions
* Locates buttons using Selenium
* Automatically performs swiping actions
* Automates repetitive clicking
* Uses loops for continuous automation
* Interacts with dynamic web elements

---

## 🧠 Concepts Learned

### Selenium WebDriver

Selenium WebDriver allows Python programs to control a web browser automatically.

It can perform actions such as:

* Open websites
* Find HTML elements
* Click buttons
* Enter text
* Read webpage content
* Navigate between pages
* Automate repetitive tasks

Example:

```python
from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://www.tinder.com/")
```

---

## 🔎 Finding Web Elements

Selenium provides different methods for locating elements.

For example:

```python
from selenium.webdriver.common.by import By

button = driver.find_element(
    By.CSS_SELECTOR,
    "button"
)
```

The element can then be clicked:

```python
button.click()
```

---

## 💕 Swiping Bot Logic

The bot follows a simple automation process:

```text
Start
  ↓
Open Chrome
  ↓
Open Tinder
  ↓
Login / Setup
  ↓
Find Swipe Buttons
  ↓
Click Like / Dislike
  ↓
Wait
  ↓
Repeat
```

The bot uses loops to perform repetitive swiping actions automatically.

---

## 🔄 Automation Workflow

The project demonstrates how Selenium can interact with a dynamic website.

```text
Python
  ↓
Selenium WebDriver
  ↓
Chrome Browser
  ↓
Tinder
  ↓
Find Web Elements
  ↓
Perform Actions
  ↓
Repeat Automation
```

---

## 📂 Project Structure

```text
Day50/
│
├── main.py
├── requirements.txt
├── README.md
│
└── screenshots/
    └── day50_output.png
```

---

## 📦 Installation

Install Selenium using:

```bash
pip install selenium
```

Or install all project dependencies:

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

Install the required package:

```bash
pip install selenium
```

Then run:

```bash
python main.py
```

The program will:

1. Open Chrome
2. Open Tinder
3. Allow login/setup
4. Find the required buttons
5. Perform automated swiping
6. Continue the process using a loop

---
# Screenshoot
<img width="1037" height="558" alt="image" src="https://github.com/user-attachments/assets/7966ea34-ca32-46db-ad07-9f86fdcf4840" />

## ⚠️ Important Note

Websites such as Tinder frequently change their page structure, element attributes, and interaction flows.

Login verification, CAPTCHA, location permissions, or other security checks may also require manual interaction.

This project is intended for **educational purposes** to learn Selenium and browser automation.

Always use automation responsibly and follow the website's terms and policies.

---

## 🎯 Learning Outcomes

By completing this project, I learned how to:

* Use Selenium WebDriver
* Automate Chrome
* Locate dynamic web elements
* Use CSS selectors and XPath
* Click buttons automatically
* Use loops for browser automation
* Handle delays using `time.sleep()`
* Work with dynamic websites
* Build practical browser automation projects

---

## 🚀 Skills Practiced

```text
Python
   ↓
Selenium
   ↓
WebDriver
   ↓
Chrome Automation
   ↓
Element Locating
   ↓
Button Interaction
   ↓
Automated Swiping
```

---

## 📚 Course

**Python Development Pro Bootcamp**

**Day 50 – Tinder Swiping Bot**

Another milestone in my Python automation journey! 🐍🤖🚀
