# 🍪 Day 48 — Cookie Clicker Game Playing Bot

## 🎯 Course

**Python Programming Pro Bootcamp**

---

## 📚 Topics Covered

On Day 48, I learned how to use **Selenium WebDriver** to control a web browser with Python and automate actions on a website.

### Main Concepts

- Selenium WebDriver
- Browser Automation
- Chrome WebDriver
- Finding HTML elements
- Clicking web elements
- Reading text from webpages
- Keyboard and mouse automation
- Working with browser windows
- Handling timers
- Automating repetitive tasks
- Game Playing Bots
- Loops and conditional logic

---

# 🍪 Project — Cookie Clicker Bot

For the Day 48 project, I built a **Cookie Clicker Game Playing Bot** using Python and Selenium.

The bot automatically opens the Cookie Clicker game, repeatedly clicks the cookie, checks the available upgrades, and purchases upgrades when possible.

Instead of manually clicking the cookie thousands of times, Selenium allows Python to control the browser and perform these actions automatically.

---

## 🔄 Project Workflow

```text
Open Chrome Browser
        ↓
Open Cookie Clicker
        ↓
Find the Cookie
        ↓
Click Cookie Repeatedly
        ↓
Check Available Upgrades
        ↓
Purchase Upgrade
        ↓
Continue Clicking
        ↓
Repeat Automatically

##📸 Screenshot
<!-- Add your project screenshot here -->

<img width="1031" height="589" alt="image" src="https://github.com/user-attachments/assets/e4cf0654-b06f-41f0-b9b0-eaded8863cb3" />


##🛠️ Technologies Used
🐍 Python
🌐 Selenium
🌍 Google Chrome
🤖 Web Automation
🎮 Game Playing Bot
💻 Project Features
Automatically opens the browser
Opens the Cookie Clicker game
Finds the cookie using Selenium
Automatically clicks the cookie
Monitors the game continuously
Checks available upgrades
Purchases upgrades automatically
Uses loops to keep the bot running
Automates repetitive gameplay

##🧩 Selenium WebDriver

Selenium WebDriver allows Python to interact with web browsers.

It can perform actions such as:

Open websites
Find HTML elements
Click buttons
Enter text
Read webpage content
Scroll pages
Control browser windows

Example:

from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://example.com")

##🔎 Finding Web Elements

Selenium provides different ways to find elements.

For example:

cookie = driver.find_element(
    by="id",
    value="bigCookie"
)

Then Selenium can click it:

cookie.click()

##🤖 Game Playing Bot Logic

The bot follows a simple automated process:

Start
  ↓
Open Game
  ↓
Find Cookie
  ↓
Click Cookie
  ↓
Check Upgrade
  ↓
Buy Upgrade
  ↓
Continue

The bot uses loops to perform repetitive actions without requiring manual clicks.

##📂 Project Structure
Day48/
│
├── main.py
├── requirements.txt
├── README.md
│
└── screenshots/
    └── day48_output.png
##📦 Installation

Install Selenium using:

pip install selenium

Or install all project dependencies:

pip install -r requirements.txt

##▶️ How to Run

Open the project folder in VS Code.

Install the required package:

pip install selenium

Then run:

python main.py

The program will automatically:

Open Chrome
Open Cookie Clicker
Find the cookie
Start clicking
Check upgrades
Purchase upgrades
Continue playing automatically
##🧠 What I Learned

Through this project, I learned:

How Selenium WebDriver works
How to control a browser using Python
How to open webpages automatically
How to find HTML elements
How to click buttons and other elements
How to read information from webpages
How to automate repetitive browser tasks
How to use loops for automation
How to create a simple game-playing bot
How browser automation can be used for real-world tasks
##📸 Screenshot
<!-- Add your project screenshot here -->
<img width="1031" height="589" alt="image" src="https://github.com/user-attachments/assets/e4cf0654-b06f-41f0-b9b0-eaded8863cb3" />

##🚀 Key Takeaway

Day 48 introduced me to Browser Automation with Selenium.

I learned that Python can control a real web browser, interact with webpage elements, and perform repetitive tasks automatically.

The Cookie Clicker project was a fun way to understand how Selenium WebDriver and automation bots work together.

##📈 100 Days of Code

Day 48 / 100 🐍🍪

Continuing my journey through the Python Programming Pro Bootcamp and learning how to automate web browsers using Python and Selenium.

#Python #PythonProgramming #Selenium #WebAutomation #BrowserAutomation #CookieClicker #Automation #100DaysOfCode #LearningInPublic
