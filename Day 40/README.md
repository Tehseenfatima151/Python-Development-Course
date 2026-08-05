# Day 40 – Capstone Project Part 2: Flight Club

## 📌 Overview

Day 40 mein humne **Cheap Flight Finder Capstone Project** ka second part complete kiya, jiska naam **Flight Club** hai.

Is part mein humne application ko aur intelligent banaya by adding **User Registration**, **Customer Management**, **Email Notifications**, aur **Cheap Flight Alerts**. Users apna email register kar sakte hain aur jab kisi destination ke liye cheap flight milti hai, application automatically unhe email notification bhej deti hai.

Is project ke through humne **Object-Oriented Programming (OOP)**, **REST APIs**, **Google Sheets**, **Email Automation**, aur **Multiple API Integration** ko practically implement kiya.

---

# ✈️ Project Goal

Application automatically:

* 👤 Registers new users
* 📧 Stores customer information
* 📊 Reads destination data from Google Sheets
* 🔍 Searches for cheap flights
* 💰 Compares current price with target price
* 📩 Sends email alerts when a cheaper flight is found

---

# ✨ Features

* 👤 Customer Registration
* 📧 Email Validation
* 📊 Google Sheets Integration
* ✈️ Flight Search
* 💰 Price Comparison
* 📩 Automatic Email Notifications
* 🔑 API Authentication
* 🌱 Environment Variables
* 📦 Object-Oriented Programming

---

# 📁 Project Structure

```text id="d4w7rb"
flight-club/
│
├── main.py
├── data_manager.py
├── flight_search.py
├── flight_data.py
├── notification_manager.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

| File                      | Description                          |
| ------------------------- | ------------------------------------ |
| `main.py`                 | Main application workflow            |
| `data_manager.py`         | Reads destinations and customer data |
| `flight_search.py`        | Searches available flights           |
| `flight_data.py`          | Stores flight information            |
| `notification_manager.py` | Sends email notifications            |

---

# 🌐 APIs & Services Used

| API / Service        | Purpose                                     |
| -------------------- | ------------------------------------------- |
| Sheety API           | Store destinations and customer information |
| Flight Search API    | Search available flights                    |
| SMTP / Email Service | Send flight deal notifications              |

---

# 👤 Customer Registration

Users register by entering:

* First Name
* Last Name
* Email Address

For better accuracy, the application asks users to enter their email twice.

Flow:

```text id="m0o0m6"
Enter Email
      ↓
Confirm Email
      ↓
Emails Match?
    ↙       ↘
  Yes        No
   ↓          ↓
Save User   Ask Again
```

---

# 📊 Google Sheets Integration

Google Sheets stores two different datasets:

### Destinations Sheet

| City  | IATA Code | Lowest Price |
| ----- | --------- | ------------ |
| Paris | CDG       | 250          |
| Tokyo | HND       | 500          |

### Customers Sheet

| First Name | Last Name | Email                                   |
| ---------- | --------- | --------------------------------------- |
| Ali        | Khan      | [ali@email.com](mailto:ali@email.com)   |
| Sara       | Ahmed     | [sara@email.com](mailto:sara@email.com) |

This acts as a lightweight cloud database for the application.

---

# ✈️ Flight Search

The application searches for flights based on:

* Departure Airport
* Destination Airport
* Travel Dates
* Lowest Available Price

The returned flight price is compared with the target price stored in Google Sheets.

---

# 💰 Price Comparison

Logic:

```text id="zohg9j"
Search Flight
      ↓
Current Price
      ↓
Compare with Target Price
      ↓
Cheaper?
   ↙       ↘
 Yes        No
 ↓           ↓
Send Email  Stop
```

Only flights cheaper than the target price trigger notifications.

---

# 📧 Email Notifications

When a cheap deal is found, every registered user receives an email containing:

* Destination City
* Flight Price
* Departure Airport
* Arrival Airport
* Travel Dates

Example:

```text id="dj6ob7"
✈️ Cheap Flight Alert!

Destination: Paris
Price: $220

Book now before prices increase!
```

This feature automates flight deal notifications.

---

# 🔐 API Authentication

Authentication is required for all external services.

Credentials such as API keys and email passwords are stored securely using environment variables.

Example:

```python id="vbmy0m"
API_KEY = os.getenv("FLIGHT_API_KEY")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
```

---

# 🌱 Environment Variables

Sensitive information stored outside the source code includes:

* Flight API Key
* Sheety Token
* Email Address
* Email Password

Benefits:

* Improved security
* Easier deployment
* Prevent accidental exposure on GitHub

---

# 🔄 Project Workflow

```text id="a3m91d"
User Registration
        ↓
Store Customer Data
        ↓
Read Destination Prices
        ↓
Search Flights
        ↓
Compare Prices
        ↓
Cheap Flight Found?
      ↙          ↘
    Yes           No
     ↓             ↓
Send Email     End Program
```

---

# 📦 Python Modules Used

| Module     | Purpose               |
| ---------- | --------------------- |
| `requests` | API Requests          |
| `smtplib`  | Send Emails           |
| `os`       | Environment Variables |
| `dotenv`   | Load .env File        |
| `datetime` | Handle Dates          |
| `json`     | Process API Responses |

---

# 🧠 Important Concepts Learned

* Object-Oriented Programming
* Multiple API Integration
* Google Sheets Automation
* Customer Management
* Email Automation
* SMTP
* API Authentication
* Environment Variables
* Price Comparison Logic
* Cloud-based Data Storage

---

# 🔒 Security Best Practices

* Never hardcode API keys or email passwords.
* Store credentials using environment variables.
* Add `.env` to `.gitignore`.
* Use secure authentication methods.
* Keep customer information private.

---

# 📸 Screenshot
<img width="1184" height="721" alt="image" src="https://github.com/user-attachments/assets/5e0e9c0c-c077-4bdf-86ce-83c1b29e9a2c" />


---

# ✅ Key Takeaways

* Extended the Cheap Flight Finder into a complete Flight Club application.
* Added customer registration and email validation features.
* Used Google Sheets to manage destinations and customer records.
* Compared live flight prices with target prices.
* Automated email notifications when cheaper flights became available.
* Strengthened skills in Object-Oriented Programming, API integration, and email automation.
* Built a real-world project by combining multiple external services into one application.

---

# 🚀 Practice Tasks

* 📱 Send alerts using SMS or WhatsApp.
* 🌍 Support multiple departure cities.
* ❤️ Allow users to save favorite destinations.
* 💲 Add support for different currencies.
* 📈 Display historical flight prices.
* 🌐 Build a web interface using Flask.
* 🤖 Schedule automatic daily flight checks.

---

# 🎯 Day 40 Summary

Day 40 completed the **Flight Club Capstone Project** by adding customer registration, email notifications, and automatic flight deal alerts. The application combines **Google Sheets**, **Flight Search APIs**, **SMTP Email Services**, and **Object-Oriented Programming** to deliver a practical, real-world flight price monitoring system.

This project strengthened concepts of **API Integration**, **Cloud-based Data Management**, **Email Automation**, **Environment Variables**, and **Software Architecture**, making it one of the most comprehensive projects in the Python Bootcamp.
