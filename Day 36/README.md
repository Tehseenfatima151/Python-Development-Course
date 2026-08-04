# Day 36 – Stock Trading News Alert Project

## 📌 Overview

Day 36 mein humne **Stock Trading News Alert Project** banaya jisme Python ki help se **Stock Market API**, **News API**, aur **SMS Notification Service** ko integrate kiya.

Is project ka main objective tha kisi company ke stock price ko monitor karna. Agar stock price ek specific percentage se zyada up ya down ho jaye, to latest news articles fetch kiye jate hain aur user ko SMS notification bheji jati hai.

Is project ke through humne **Multiple APIs**, **HTTP Requests**, **JSON Data Parsing**, **API Authentication**, aur **Automation** ko practically implement kiya.

---

# 📈 Project Goal

Application automatically:

* 📊 Gets latest stock prices
* 📉 Calculates percentage change
* 📰 Fetches latest company news
* 📱 Sends SMS alert if significant price movement is detected

---

# ✨ Features

* 📊 Stock Price Monitoring
* 📉 Percentage Change Calculation
* 📰 News API Integration
* 📱 SMS Notifications
* 🔑 API Authentication
* 🌱 Environment Variables
* 🤖 Automated Stock Alerts
* 📄 JSON Data Processing

---

# 📁 Project Structure

```text
stock-news-alert/
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🌐 APIs Used

| API               | Purpose                   |
| ----------------- | ------------------------- |
| Alpha Vantage API | Fetch daily stock prices  |
| NewsAPI           | Fetch latest company news |
| Twilio API        | Send SMS notifications    |

---

# 🔑 API Keys

The project requires authentication for all APIs.

Example:

```python
STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
```

Sensitive information should never be hardcoded inside the source code.

---

# 🌱 Environment Variables

Environment variables are used to securely store:

* Alpha Vantage API Key
* News API Key
* Twilio Account SID
* Twilio Auth Token
* Phone Numbers

Benefits:

* Better security
* Easy deployment
* Prevent exposing secrets on GitHub

---

# 📊 Stock Price Monitoring

The application requests daily stock data.

Example information received:

* Opening Price
* Closing Price
* Highest Price
* Lowest Price
* Trading Volume

The latest two trading days are compared.

Example:

```text
Yesterday : $180
Today      : $186
Difference : +6
```

---

# 📉 Percentage Change

Formula:

```text
Percentage Change

(Current Price - Previous Price)
-------------------------------- × 100
      Previous Price
```

If price movement is greater than **5%**, the application proceeds to fetch news.

Logic:

```text
Get Stock Data
        ↓
Calculate Percentage
        ↓
Movement > 5% ?
      ↙        ↘
    Yes         No
     ↓           ↓
Fetch News    Stop
```

---

# 📰 News API

If significant price movement is detected, the application requests the latest news related to that company.

Information fetched:

* News Headline
* News Description
* News Source
* Published Date

Only the top few articles are selected.

---

# 📱 SMS Notification

The project uses **Twilio API** to send alerts.

Example SMS:

```text
TSLA: 🔺5%

Headline:
Tesla announces new AI feature.

Brief:
The company revealed...
```

Each SMS contains:

* Stock Symbol
* Price Movement
* News Headline
* Short Description

---

# 🔄 Project Workflow

```text
Start Program
      ↓
Fetch Stock Data
      ↓
Calculate Percentage Change
      ↓
Price Movement > 5% ?
      ↓
Fetch Latest News
      ↓
Prepare SMS
      ↓
Send Notification
```

---

# 📦 Python Modules Used

| Module     | Purpose               |
| ---------- | --------------------- |
| `requests` | API Requests          |
| `json`     | Process API Responses |
| `os`       | Environment Variables |
| `datetime` | Handle Dates          |
| `twilio`   | Send SMS              |

---

# 🧠 Important Concepts Learned

* REST APIs
* API Authentication
* Multiple API Integration
* JSON Parsing
* HTTP Requests
* Environment Variables
* Percentage Calculations
* Stock Market Data
* News APIs
* SMS Automation
* Secure Credential Management

---

# 🔒 Security Best Practices

* Never hardcode API keys.
* Store credentials in environment variables.
* Add `.env` to `.gitignore`.
* Rotate API keys if exposed.
* Keep authentication tokens private.

---

# 📸 Screenshot

*Add your Stock News Alert project screenshots here.*

<img width="1194" height="727" alt="1" src="https://github.com/user-attachments/assets/e792a085-5d19-465d-ac78-273d0a366c50" />


---

# ✅ Key Takeaways

* Learned to integrate multiple third-party APIs in a single Python project.
* Retrieved live stock market data using the Alpha Vantage API.
* Calculated daily percentage changes in stock prices.
* Used NewsAPI to fetch recent articles related to a company.
* Automated SMS notifications using Twilio.
* Improved skills in JSON parsing, HTTP requests, and API authentication.
* Practiced building real-world automation projects using Python.

---

# 🚀 Practice Tasks

* 📈 Monitor multiple companies at the same time.
* 📧 Send alerts through Email in addition to SMS.
* 📱 Add WhatsApp notifications.
* 📊 Display stock price charts.
* 📅 Monitor weekly or monthly stock trends.
* 💾 Save stock history in a database.
* 🤖 Schedule automatic monitoring every morning.

---

# 🎯 Day 36 Summary

Day 36 introduced a real-world automation project by combining **Stock Market APIs**, **News APIs**, and **SMS Notifications** into one application. The project continuously monitors stock prices, calculates percentage changes, retrieves relevant news, and notifies the user whenever a significant market movement occurs.

This project strengthened concepts of **API Integration**, **Authentication**, **Environment Variables**, **JSON Processing**, and **Automation**, making it an excellent example of building practical, production-style Python applications.
