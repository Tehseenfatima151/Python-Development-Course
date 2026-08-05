# Day 37 – Advanced Authentication & HTTP Requests (POST, PUT, DELETE)

## 📌 Overview

Day 37 mein humne **Advanced API Authentication** aur different **HTTP Request Methods** (`GET`, `POST`, `PUT`, `DELETE`) ko practically seekha. Is project mein humne **Pixela API** use karke ek **Habit Tracker** banaya jisme user apni daily activities (jaise coding, exercise, reading, etc.) ko graph ke form mein track kar sakta hai.

Is project ke through humne **API Authentication**, **HTTP Methods**, **JSON Requests**, aur **REST APIs** ko real-world example ke sath implement kiya.

---

# 🎯 Project Goal

Application allows users to:

* 👤 Create a new account
* 📊 Create a habit graph
* ➕ Add daily progress
* ✏️ Update existing records
* 🗑️ Delete records
* 📈 Track habits visually

---

# ✨ Features

* 🔐 Advanced API Authentication
* 👤 User Registration
* 📊 Graph Creation
* ➕ Add Daily Data
* ✏️ Update Existing Data
* 🗑️ Delete Data
* 📅 Daily Habit Tracking
* 🌐 REST API Integration

---

# 📁 Project Structure

```text
habit-tracker/
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🌐 API Used

| API        | Purpose                         |
| ---------- | ------------------------------- |
| Pixela API | Track daily habits using graphs |

---

# 🔐 Advanced Authentication

Unlike previous projects that only used API Keys, Pixela uses a **Username + Token** authentication system.

Example:

```python
USERNAME = os.getenv("PIXELA_USERNAME")
TOKEN = os.getenv("PIXELA_TOKEN")
```

Every protected request includes authentication headers.

```python
headers = {
    "X-USER-TOKEN": TOKEN
}
```

This verifies the identity of the user before allowing access to data.

---

# 🌱 Environment Variables

Sensitive credentials are stored using environment variables.

Examples:

* Username
* Token
* Graph ID

Benefits:

* Better security
* Easier deployment
* Prevent secrets from being uploaded to GitHub

---

# 🌍 REST API

REST APIs communicate using different HTTP request methods.

| Method | Purpose              |
| ------ | -------------------- |
| GET    | Retrieve data        |
| POST   | Create new data      |
| PUT    | Update existing data |
| DELETE | Remove data          |

---

# ➕ POST Request

A **POST** request is used to create new resources.

Examples:

* Create User
* Create Graph
* Add Daily Pixel

Example:

```python
requests.post(url=PIXELA_ENDPOINT, json=user_data)
```

Flow:

```text
Client
   ↓
POST Request
   ↓
Server
   ↓
New Resource Created
```

---

# ✏️ PUT Request

A **PUT** request updates existing data.

Example:

* Correct today's coding hours
* Update exercise record

Example:

```python
requests.put(url=update_endpoint, json=new_data, headers=headers)
```

Flow:

```text
Existing Data
      ↓
PUT Request
      ↓
Updated Data
```

---

# 🗑️ DELETE Request

DELETE removes existing records.

Example:

```python
requests.delete(url=delete_endpoint, headers=headers)
```

Flow:

```text
Existing Record
        ↓
DELETE Request
        ↓
Record Removed
```

---

# 📊 Habit Tracking

The project records daily activities.

Example:

```text
Date : 2026-08-04
Coding : 5 Hours
```

Every entry appears as a colored pixel on the graph.

More work = More graph activity.

---

# 📈 Graph Visualization

Pixela automatically converts daily entries into a contribution graph similar to GitHub.

Example:

```text
⬜ 🟩 🟩 🟨 🟩
🟩 🟩 ⬜ 🟩 🟩
🟩 🟨 🟩 🟩 ⬜
```

This makes it easy to visualize consistency over time.

---

# 🔄 Project Workflow

```text
Create User
      ↓
Create Graph
      ↓
Add Daily Data
      ↓
View Habit Graph
      ↓
Update Data (PUT)
      ↓
Delete Data (DELETE)
```

---

# 📦 Python Modules Used

| Module     | Purpose                    |
| ---------- | -------------------------- |
| `requests` | Send HTTP Requests         |
| `os`       | Read Environment Variables |
| `datetime` | Generate Current Date      |
| `json`     | Process JSON Data          |

---

# 🧠 Important Concepts Learned

* REST APIs
* Advanced Authentication
* Environment Variables
* HTTP Methods
* GET Requests
* POST Requests
* PUT Requests
* DELETE Requests
* JSON Requests
* Headers
* API Endpoints
* Habit Tracking
* Graph APIs

---

# 🔒 Security Best Practices

* Never hardcode authentication tokens.
* Store credentials in environment variables.
* Add `.env` to `.gitignore`.
* Keep API tokens private.
* Rotate tokens if they become exposed.

---

# 📸 Screenshot

*Add your Habit Tracker project screenshots here.*
<img width="1195" height="723" alt="1" src="https://github.com/user-attachments/assets/b67d3368-003d-413f-8542-31784f2f60ff" />



---

# ✅ Key Takeaways

* Learned how advanced API authentication works using authentication tokens.
* Practiced all major HTTP request methods: **GET**, **POST**, **PUT**, and **DELETE**.
* Built a habit tracker using the Pixela REST API.
* Stored sensitive credentials securely with environment variables.
* Sent JSON data in API requests and processed API responses.
* Understood how RESTful APIs are used to create, update, retrieve, and delete resources.
* Built a real-world application that tracks daily habits visually through graphs.

---

# 🚀 Practice Tasks

* 📚 Track daily study hours.
* 💧 Create a water intake tracker.
* 🏃 Track daily exercise.
* 💰 Track daily expenses.
* 😴 Record sleeping hours.
* 📖 Track book reading progress.
* 📈 Create multiple habit graphs for different activities.

---

# 🎯 Day 37 Summary

Day 37 introduced **Advanced Authentication** and the four major HTTP request methods used in REST APIs. Using the Pixela API, we built a Habit Tracker that allows users to create graphs, add daily progress, update records, and delete entries. This project strengthened concepts of **API Authentication**, **RESTful Services**, **Environment Variables**, **JSON Requests**, and **HTTP Methods**, making it an excellent introduction to building real-world API-based applications.
