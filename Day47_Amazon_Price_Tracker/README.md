# 🛒 Day 47 — Amazon Price Tracker

## 🎯 Course

**Python Programming Pro Bootcamp**

---

## 📚 Topics Covered

On Day 47, I built an **Automated Amazon Price Tracker** using Python.

### Main Concepts

- Web Scraping
- BeautifulSoup
- Requests
- HTML parsing
- CSS selectors
- Extracting product title and price
- Environment variables
- Email automation
- SMTP
- `smtplib`
- `email.message`
- Conditional logic
- Automating price alerts

---

# 🛍️ Project — Automated Amazon Price Tracker

The **Amazon Price Tracker** checks the price of a product on Amazon and sends an email notification when the price drops below a target price.

Instead of checking the product manually, Python can automatically monitor the price and notify the user when it reaches the desired amount.

---

## 🔄 Project Workflow

```text
Amazon Product URL
        ↓
Requests
        ↓
Amazon HTML
        ↓
BeautifulSoup
        ↓
Extract Product Price
        ↓
Compare With Target Price
        ↓
Price ≤ Target?
      ↙     ↘
    YES      NO
     ↓        ↓
Send Email   No Alert
```

---

## 🛠️ Technologies Used

- 🐍 Python
- 🌐 Requests
- 🍲 BeautifulSoup
- 📧 SMTP
- 🔐 Environment Variables
- 📄 HTML Parsing

---

## 💻 Project Features

- Checks an Amazon product page
- Extracts the product title
- Extracts the current price
- Compares the current price with a target price
- Sends an email when the price is low enough
- Keeps email credentials in `.env`
- Can be automated with Windows Task Scheduler or another scheduler

---

## 📂 Project Structure

```text
Day47/
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
├── README.md
│
└── screenshots/
    └── day47_output.png
```

---

## 📦 Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
PRODUCT_URL=https://www.amazon.com/dp/REPLACE_WITH_PRODUCT_ID
TARGET_PRICE=100

EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
TO_EMAIL=your_email@gmail.com
```

### Important

Do **not** upload `.env` to GitHub because it contains private credentials.

The `.gitignore` file already contains:

```text
.env
```

---

## 📧 Gmail App Password

If you use Gmail for sending alerts, use a **Gmail App Password** instead of your normal Gmail password.

Your Google account may require **2-Step Verification** before an App Password can be created.

---

## ▶️ How to Run

Open the Day47 folder in VS Code.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

Example:

```text
Checking Amazon product price...

Product: Example Product
Current price: 89.99
Target price: 100

🎉 Price is below your target!
Email alert sent successfully.
```

---

## ⏰ Automation

The program can be scheduled to run automatically.

For example, on Windows you can use **Task Scheduler** to run:

```bash
python main.py
```

at a chosen time every day.

This turns the project into an automated price-monitoring system.

---

## 🧠 What I Learned

Through this project, I learned:

- How to scrape information from web pages
- How to use BeautifulSoup
- How to find HTML elements with CSS selectors
- How to extract and convert prices
- How to compare values using Python
- How SMTP email works
- How to send automated emails
- How to protect credentials with environment variables
- How Python can automate real-world tasks

---

## 📸 Screenshot

<!-- Add your project screenshot here -->


<img width="1186" height="714" alt="image" src="https://github.com/user-attachments/assets/9a09b8b7-4bbc-4ab2-bfa8-55c66bc269a4" />

---


## 🚀 Key Takeaway

Day 47 taught me how to combine **web scraping, conditional logic, email automation, and environment variables** to build a useful real-world Python automation project.

Instead of manually checking prices, the program can monitor a product and notify me when the price reaches my target.

---

## 📈 100 Days of Code

**Day 47 / 100** 🐍🛒

Continuing my journey through the **Python Programming Pro Bootcamp** and building practical automation projects.

#Python #PythonProgramming #WebScraping #BeautifulSoup #AmazonPriceTracker #Automation #SMTP #100DaysOfCode #LearningInPublic
