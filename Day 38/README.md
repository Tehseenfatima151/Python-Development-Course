# Day 38 – Exercise Tracking with Python & Google Sheets

## 📌 Overview

Day 38 mein humne **Exercise Tracking Application** banai jo Natural Language Processing (NLP), APIs aur Google Sheets ko combine karti hai.

Is project ka main objective tha user se normal English sentence lena (jaise *"I ran for 30 minutes and cycled for 10 minutes"*), us sentence ko analyze karna, calories aur exercise details calculate karna, aur automatically Google Sheets mein save karna.

Is project ke through humne **Natural Language APIs**, **POST Requests**, **API Authentication**, **Environment Variables**, aur **Google Sheets Integration** ko practically implement kiya.

---

# 🎯 Project Goal

Application automatically:

* 📝 Accepts exercise description in plain English
* 🤖 Uses NLP to understand the activity
* 🔥 Calculates calories burned
* ⏱️ Calculates exercise duration
* 📅 Records date and time
* 📊 Saves all information into Google Sheets

---

# ✨ Features

* 🤖 Natural Language Processing (NLP)
* 🏃 Exercise Recognition
* 🔥 Calorie Estimation
* ⏱️ Exercise Duration Tracking
* 📅 Automatic Date & Time
* 📊 Google Sheets Integration
* 🔑 API Authentication
* 🌱 Environment Variables

---

# 📁 Project Structure

```text
exercise-tracker/
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🌐 APIs Used

| API             | Purpose                                |
| --------------- | -------------------------------------- |
| Nutritionix API | Detect exercises and estimate calories |
| Sheety API      | Save exercise data into Google Sheets  |

---

# 🤖 Natural Language Processing

Instead of entering exercise details manually, the user simply writes a sentence like:

```text
I walked for 45 minutes and ran for 20 minutes.
```

The Nutritionix API extracts:

* Exercise Name
* Duration
* Calories Burned

This makes the application much easier and more user-friendly.

---

# 🔑 API Authentication

Both APIs require authentication before processing requests.

Example credentials:

* Nutritionix App ID
* Nutritionix API Key
* Sheety Authentication Token

These credentials should be stored securely using environment variables.

---

# 🌱 Environment Variables

Sensitive information is stored outside the source code.

Example:

```python
APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")
SHEETY_TOKEN = os.getenv("SHEETY_TOKEN")
```

Benefits include:

* Better security
* Easy deployment
* Prevent exposing secrets on GitHub

---

# 🏃 Exercise Detection

The Nutritionix API analyzes the user's sentence and returns:

* Exercise Name
* Duration (Minutes)
* Calories Burned

Example response:

```text
Exercise : Running
Duration : 30 Minutes
Calories : 320 kcal
```

---

# 📅 Date & Time

The application automatically records:

* Current Date
* Current Time

Example:

```text
Date : 05/08/2026
Time : 06:30 PM
```

This helps maintain an accurate workout history.

---

# 📊 Google Sheets Integration

Instead of saving data locally, the project stores it directly in Google Sheets.

Each exercise is added as a new row.

Example:

| Date       | Time     | Exercise | Duration | Calories |
| ---------- | -------- | -------- | -------- | -------- |
| 05/08/2026 | 06:30 PM | Running  | 30 min   | 320      |

This allows users to access their workout log from anywhere.

---

# ➕ POST Request

The project sends exercise information using an HTTP **POST** request.

Flow:

```text
Exercise Data
      ↓
POST Request
      ↓
Sheety API
      ↓
Google Sheet Updated
```

Each workout automatically becomes a new spreadsheet entry.

---

# 🔄 Project Workflow

```text
User Enters Exercise
         ↓
Nutritionix API
         ↓
Exercise Details
         ↓
Current Date & Time
         ↓
Sheety API
         ↓
Google Sheets Updated
```

---

# 📦 Python Modules Used

| Module     | Purpose               |
| ---------- | --------------------- |
| `requests` | Send HTTP Requests    |
| `datetime` | Current Date & Time   |
| `os`       | Environment Variables |
| `dotenv`   | Load .env File        |

---

# 🧠 Important Concepts Learned

* REST APIs
* API Authentication
* Natural Language Processing (NLP)
* Environment Variables
* HTTP POST Requests
* JSON Requests & Responses
* Google Sheets Automation
* Date & Time Handling
* Third-party API Integration

---

# 🔒 Security Best Practices

* Never hardcode API keys.
* Store credentials in environment variables.
* Add `.env` to `.gitignore`.
* Keep authentication tokens private.
* Rotate API keys if they become exposed.

---

# 📸 Screenshot

<img width="1201" height="723" alt="1" src="https://github.com/user-attachments/assets/465f51ff-0ce7-470d-8a0d-238b034af10c" />


---

# ✅ Key Takeaways

* Learned how Natural Language Processing can understand plain English exercise descriptions.
* Integrated the Nutritionix API to calculate exercise duration and calories burned.
* Stored workout records automatically in Google Sheets using the Sheety API.
* Used HTTP POST requests to send structured data to external services.
* Secured API credentials using environment variables.
* Combined multiple APIs to build a practical fitness tracking application.

---

# 🚀 Practice Tasks

* 🚶 Track multiple exercises in one sentence.
* 📏 Add support for distance tracking.
* 💧 Record daily water intake.
* ⚖️ Calculate BMI before logging workouts.
* 📈 Create charts from Google Sheets data.
* 📧 Send a daily workout summary by email.
* 📱 Build a mobile version using Flutter.

---

# 🎯 Day 38 Summary

Day 38 focused on building a real-world **Exercise Tracking Application** using Python, Natural Language Processing, and Google Sheets. The project accepts exercise descriptions in everyday English, analyzes them using the Nutritionix API, calculates workout statistics, and stores the results automatically in Google Sheets through the Sheety API.

This project strengthened concepts of **API Integration**, **NLP**, **POST Requests**, **Environment Variables**, **Google Sheets Automation**, and **Cloud-based Data Storage**, making it an excellent example of a practical Python automation project.
