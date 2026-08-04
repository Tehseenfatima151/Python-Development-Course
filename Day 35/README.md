# Day 35 – API Keys, Authentication, Environment Variables & Sending SMS

## 📌 Overview

Day 35 mein humne **API Authentication**, **Environment Variables**, aur **SMS Notifications** ke concepts seekhe. Is project ka main objective tha multiple APIs ko integrate karke ek **Weather Alert System** banana jo weather forecast check kare aur agar rain expected ho to user ko SMS notification bheje.

Is project ke through humne **API Keys**, **Authentication**, **Environment Variables**, **HTTP Requests**, aur **Twilio SMS API** ko practically implement kiya.

---

# 🌦️ Project Goal

Application automatically:

* 🌍 Gets weather forecast using Weather API
* ☁️ Checks upcoming weather conditions
* 🌧️ Detects possible rain
* 📱 Sends an SMS alert if rain is expected

---

# ✨ Features

* 🌤️ Weather Forecast API Integration
* 🔑 API Key Authentication
* 🌍 Location-based Forecast
* 🌧️ Rain Detection
* 📱 SMS Notification
* 🔒 Secure API Key Storage
* 🌱 Environment Variables
* 🤖 Automatic Weather Checking

---

# 📁 Project Structure

```text
weather-alert/
│
├── main.py
├── .env (optional)
└── README.md
```

---

# 🌐 APIs Used

The project integrates two APIs:

| API             | Purpose                |
| --------------- | ---------------------- |
| OpenWeather API | Fetch weather forecast |
| Twilio API      | Send SMS notifications |

---

# 🔑 API Keys

Most web APIs require authentication before allowing access.

Example:

```python
API_KEY = os.environ.get("OWM_API_KEY")
```

Instead of hardcoding the key inside the source code, it is stored securely using environment variables.

---

# 🔐 Authentication

Authentication verifies that the request is coming from an authorized user.

Without a valid API key:

* Request is rejected
* API returns an authentication error
* Data cannot be accessed

---

# 🌱 Environment Variables

Environment Variables store sensitive information outside the source code.

Examples:

* Weather API Key
* Twilio Account SID
* Twilio Auth Token
* Phone Numbers

Example:

```python
import os

API_KEY = os.environ.get("OWM_API_KEY")
```

### Why use Environment Variables?

* Improve security
* Prevent exposing secret keys on GitHub
* Make applications easier to deploy
* Separate configuration from source code

---

# 🌦️ Weather API

The Weather API provides forecast information such as:

* Temperature
* Humidity
* Weather Condition
* Rain Forecast
* Wind Speed

The application requests forecast data for a specific latitude and longitude.

Example request parameters:

```python
parameters = {
    "lat": LATITUDE,
    "lon": LONGITUDE,
    "appid": API_KEY,
    "cnt": 4
}
```

---

# 🌧️ Rain Detection

After receiving forecast data, the application checks weather condition codes.

Logic:

```text
Weather Forecast
        ↓
Read Weather Codes
        ↓
Rain Expected?
     ↙       ↘
   Yes        No
    ↓          ↓
Send SMS    Do Nothing
```

Weather condition IDs below **700** generally indicate rain, snow or other precipitation.

---

# 📱 Sending SMS

The project uses **Twilio** to send SMS alerts.

SMS example:

```text
🌧️ It's going to rain today.
Remember to bring an umbrella!
```

Twilio requires:

* Account SID
* Auth Token
* Verified Phone Number

These credentials should also be stored as environment variables.

---

# 🔄 Project Workflow

```text
Start Program
      ↓
Read Environment Variables
      ↓
Request Weather Data
      ↓
Receive Forecast
      ↓
Check Weather Codes
      ↓
Rain Expected?
   ↙          ↘
 Yes          No
 ↓             ↓
Send SMS    End Program
```

---

# 📦 Python Modules Used

| Module     | Purpose                    |
| ---------- | -------------------------- |
| `requests` | Send HTTP requests         |
| `os`       | Read environment variables |
| `twilio`   | Send SMS                   |
| `json`     | Handle API responses       |

---

# 🧠 Important Concepts Learned

* REST APIs
* API Authentication
* API Keys
* HTTP Requests
* Query Parameters
* JSON Responses
* Environment Variables
* Secure Credential Management
* Weather Forecast APIs
* SMS Automation
* Third-party API Integration

---

# 🔒 Security Best Practices

* Never hardcode API keys.
* Store secrets in environment variables.
* Do not upload API credentials to GitHub.
* Add sensitive files such as `.env` to `.gitignore`.
* Rotate API keys if they are accidentally exposed.

---

# 📸 Screenshot

*Add your Weather Alert project screenshots here.*

<img width="1200" height="722" alt="1" src="https://github.com/user-attachments/assets/24fae8ed-3758-4e4e-b059-a40bae21d9b0" />


---

# ✅ Key Takeaways

* Learned how to authenticate API requests using API keys.
* Used environment variables to securely store sensitive credentials.
* Integrated the OpenWeather API to retrieve weather forecasts.
* Parsed JSON responses returned by web APIs.
* Implemented logic to detect rainy weather conditions.
* Sent automated SMS alerts using the Twilio API.
* Followed security best practices by avoiding hardcoded credentials.

---

# 🚀 Practice Tasks

* 📧 Send weather alerts via Email.
* 📍 Allow users to search weather by city name.
* 🌡️ Display temperature and humidity in the SMS.
* ⏰ Schedule automatic weather checks every morning.
* 🌎 Support multiple locations.
* 📲 Send notifications using WhatsApp instead of SMS.
* 🌦️ Add weather icons in the notification.

---

# 🎯 Day 35 Summary

Day 35 introduced real-world API integration by combining **Weather APIs**, **Authentication**, **Environment Variables**, and **SMS Automation**. Instead of building a standalone application, this project demonstrated how multiple online services can work together to automate useful tasks such as sending weather alerts.

This project strengthened concepts of secure credential management, REST APIs, JSON handling, and third-party service integration, making it an important step toward building production-ready Python applications.
