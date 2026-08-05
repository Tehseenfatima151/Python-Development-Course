# Day 39 – Capstone Project Part 1: Cheap Flight Finder

## 📌 Overview

Day 39 mein humne **Cheap Flight Finder** capstone project ka pehla part shuru kiya. Is project ka main objective tha users ko **cheap flight deals** dhoondhne mein help karna by integrating multiple APIs.

Application destination cities ki information Google Sheets se read karti hai, har city ka **IATA Airport Code** search karti hai, aur phir us information ko update karti hai. Ye data project ke next parts mein cheap flight prices search karne ke liye use hota hai.

Is project ke through humne **Object-Oriented Programming (OOP)**, **REST APIs**, **Google Sheets**, **API Authentication**, aur **Data Management** ko practically implement kiya.

---

# ✈️ Project Goal

Application automatically:

* 📊 Reads destination cities from Google Sheets
* 🌍 Searches IATA Airport Codes
* 🔄 Updates missing airport codes
* 📄 Stores updated information
* 🚀 Prepares data for flight price searching

---

# ✨ Features

* ✈️ Flight Data Management
* 🌍 IATA Code Lookup
* 📊 Google Sheets Integration
* 🔑 API Authentication
* 🌱 Environment Variables
* 📦 Object-Oriented Programming
* 🔄 Automatic Data Updates
* 🤖 API Automation

---

# 📁 Project Structure

```text
cheap-flight-finder/
│
├── main.py
├── data_manager.py
├── flight_search.py
├── flight_data.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

| File               | Description                            |
| ------------------ | -------------------------------------- |
| `main.py`          | Main application workflow              |
| `data_manager.py`  | Reads and updates Google Sheets        |
| `flight_search.py` | Searches airport information using API |
| `flight_data.py`   | Stores flight-related data objects     |

---

# 🌐 APIs Used

| API                | Purpose                     |
| ------------------ | --------------------------- |
| Sheety API         | Read & Update Google Sheets |
| Tequila (Kiwi) API | Search IATA Airport Codes   |

---

# 🏗️ Object-Oriented Design

The project is divided into separate classes.

### `DataManager`

Responsible for:

* Reading destination data
* Updating Google Sheets
* Managing spreadsheet records

---

### `FlightSearch`

Responsible for:

* Searching airport information
* Returning IATA codes
* Communicating with the Flight API

---

### `FlightData`

Stores information related to flights and airports.

This separation keeps the code clean, reusable and easier to maintain.

---

# 🌍 What is an IATA Code?

An **IATA Code** is a unique three-letter airport identifier assigned by the International Air Transport Association.

Examples:

| City    | Airport Code |
| ------- | ------------ |
| Lahore  | LHE          |
| Karachi | KHI          |
| Dubai   | DXB          |
| London  | LHR          |
| Paris   | CDG          |

Instead of searching airports manually, the application retrieves these codes automatically.

---

# 📊 Google Sheets Integration

Google Sheets acts as a simple cloud database.

Initially the sheet may look like:

| City   | IATA Code |
| ------ | --------- |
| Paris  |           |
| Tokyo  |           |
| Berlin |           |

After running the application:

| City   | IATA Code |
| ------ | --------- |
| Paris  | CDG       |
| Tokyo  | HND       |
| Berlin | BER       |

The missing airport codes are automatically filled.

---

# 🔑 API Authentication

The application authenticates requests using API keys stored securely as environment variables.

Example:

```python
API_KEY = os.getenv("TEQUILA_API_KEY")
```

Sensitive information should never be written directly inside the source code.

---

# 🌱 Environment Variables

Environment variables store:

* Flight API Key
* Sheety Token
* Spreadsheet Endpoint

Benefits:

* Better security
* Easier deployment
* Prevent accidental exposure of credentials

---

# 🔄 Project Workflow

```text
Start Program
      ↓
Read Google Sheets
      ↓
Find Missing IATA Codes
      ↓
Call Flight API
      ↓
Receive Airport Codes
      ↓
Update Google Sheets
      ↓
Ready for Flight Search
```

---

# 📦 Python Modules Used

| Module     | Purpose               |
| ---------- | --------------------- |
| `requests` | API Requests          |
| `os`       | Environment Variables |
| `dotenv`   | Load .env File        |
| `json`     | Handle API Responses  |

---

# 🧠 Important Concepts Learned

* Object-Oriented Programming
* Classes & Objects
* REST APIs
* API Authentication
* Environment Variables
* Google Sheets Automation
* JSON Data Handling
* API Integration
* Data Management
* Cloud-based Storage

---

# 🔒 Security Best Practices

* Store API keys in environment variables.
* Never upload `.env` files to GitHub.
* Add `.env` to `.gitignore`.
* Keep authentication tokens private.
* Avoid hardcoding sensitive information.

---

# 📸 Screenshot

<img width="1180" height="705" alt="image" src="https://github.com/user-attachments/assets/0750e119-ec41-45be-bdf9-bfa9b13db063" />


---

# ✅ Key Takeaways

* Built the foundation of a real-world Flight Deal Finder application.
* Practiced Object-Oriented Programming by separating responsibilities into multiple classes.
* Integrated Google Sheets as a cloud-based data source.
* Used the Tequila API to retrieve airport IATA codes automatically.
* Learned how APIs can work together to automate repetitive tasks.
* Improved code organization by separating data management from business logic.

---

# 🚀 Practice Tasks

* 🌍 Add support for more destination cities.
* ✈️ Display airport names along with IATA codes.
* 📊 Validate duplicate city entries.
* 🌐 Support multiple countries.
* 🔍 Search airports by country instead of city.
* 📄 Export destination data as CSV.
* 📱 Build a simple GUI for managing destinations.

---

# 🎯 Day 39 Summary

Day 39 marked the beginning of the **Cheap Flight Finder Capstone Project**. In this part, we built the application's foundation by integrating Google Sheets with a Flight Search API to automatically retrieve and update airport IATA codes. The project emphasized **Object-Oriented Programming**, **API Integration**, **Environment Variables**, and **Cloud-based Data Management**, preparing the application for flight price searching in the next stages.
