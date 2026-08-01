# Day 30 – Errors, Exceptions & Saving JSON Data

## 📌 Overview

Day 30 mein humne **Password Manager** project ko aur improve kiya by adding **Error Handling**, **Exceptions**, aur **JSON Data Storage**.

Day 29 mein passwords sirf **text file (`data.txt`)** mein save ho rahe thay. Day 30 mein humne unhe **JSON format** mein store karna seekha, jisse data ko organize karna aur search karna bohot easy ho gaya.

Is project mein humne **try-except-else-finally**, **JSON module**, **dictionary manipulation**, aur **password search functionality** implement ki.

---

# 🚀 What's New in Day 30?

Compared to Day 29, the following improvements were added:

* 📂 Passwords saved in **JSON** instead of text file
* 🔍 Search Password feature
* ⚠️ Proper Exception Handling
* 📄 Automatic JSON file creation
* 🔄 Existing data update without deleting old records
* ✅ Better user experience using message boxes

---

# ✨ Features

* 🖥️ Tkinter GUI
* 🔑 Strong Password Generator
* 📋 Automatic Clipboard Copy
* 💾 Save Passwords in JSON
* 🔍 Search Saved Passwords
* ⚠️ Exception Handling
* 📄 Automatic JSON File Creation
* ✅ Input Validation
* 💬 Confirmation & Information Dialogs

---

# 📁 Project Structure

```text
password-manager/
│
├── main.py
├── logo.png
└── data.json
```

| File        | Description                         |
| ----------- | ----------------------------------- |
| `main.py`   | Main application logic              |
| `logo.png`  | Password Manager logo               |
| `data.json` | Stores all passwords in JSON format |

---

# 📄 Why JSON Instead of Text File?

Day 29 stored data like this:

```text
Google | abc@gmail.com | password123
Facebook | xyz@gmail.com | hello456
```

Searching data from a text file becomes difficult.

Day 30 stores data as structured JSON:

```json
{
    "Google": {
        "email": "abc@gmail.com",
        "password": "password123"
    },
    "Facebook": {
        "email": "xyz@gmail.com",
        "password": "hello456"
    }
}
```

JSON makes data easier to read, update and search.

---

# 🔑 Password Generator

Password generation remains the same as Day 29.

The application creates a strong password using:

* Letters
* Numbers
* Symbols

Functions used:

```python
choice()
randint()
shuffle()
```

Generated password is automatically copied using:

```python
pyperclip.copy(password)
```

---

# 💾 Saving Passwords

Instead of writing plain text, passwords are now stored inside a Python dictionary.

Example:

```python
new_data = {
    website: {
        "email": email,
        "password": password
    }
}
```

If the JSON file already exists:

* Existing data is loaded
* New record is added
* Updated data is saved back

This prevents previous passwords from being lost.

---

# 🔄 Updating Existing Data

Existing data is loaded using:

```python
data = json.load(data_file)
```

New website information is added using:

```python
data.update(new_data)
```

Finally everything is saved:

```python
json.dump(data, data_file, indent=4)
```

`indent=4` makes the JSON file nicely formatted and readable.

---

# ⚠️ Error Handling

Day 30 introduced **Exception Handling**.

Structure used:

```python
try:
    ...
except:
    ...
else:
    ...
finally:
    ...
```

### `try`

Attempts to open the JSON file.

### `except FileNotFoundError`

If the file doesn't exist, Python automatically creates a new `data.json` file.

### `else`

Runs only if no error occurs. Existing data is updated here.

### `finally`

Always executes. Used to clear input fields after saving.

---

# 🔍 Search Password Feature

A brand new **Search** button was added.

When the user enters a website name:

* JSON file is opened
* Website is searched
* Email and Password are displayed

If website exists:

```text
Website Found
      ↓
Email
Password
```

Otherwise:

```text
No details for this website exist.
```

If the JSON file itself is missing:

```text
No Data File Found.
```

---

# 💬 Message Boxes

The project uses Tkinter's **messagebox** module for user interaction.

Functions used:

```python
messagebox.showinfo()
```

Used for:

* Empty field warning
* Search results
* Error messages

---

# 🎨 Tkinter Widgets Used

| Widget       | Purpose                   |
| ------------ | ------------------------- |
| `Tk()`       | Main window               |
| `Canvas`     | Logo display              |
| `PhotoImage` | Load image                |
| `Label`      | Display text              |
| `Entry`      | User input                |
| `Button`     | Generate, Search and Save |
| `messagebox` | Dialog boxes              |

---

# ⚙️ Application Flow

```text
Open Application
        ↓
Enter Website
        ↓
Generate Password
        ↓
Password Copied
        ↓
Click Add
        ↓
Read JSON File
        ↓
Update Dictionary
        ↓
Save JSON
```

Search Flow:

```text
Enter Website
        ↓
Click Search
        ↓
Open JSON
        ↓
Website Found?
      ↙        ↘
    Yes         No
     ↓          ↓
Show Email   Error Message
Show Password
```

---

# 🧠 Important Concepts Learned

* Exception Handling
* `try`
* `except`
* `else`
* `finally`
* JSON Module
* `json.load()`
* `json.dump()`
* Dictionary Update
* File Handling
* Search Functionality
* Clipboard (`pyperclip`)
* Tkinter GUI
* Message Boxes
* Data Validation

---

# 📸 Screenshot
<img width="835" height="582" alt="1" src="https://github.com/user-attachments/assets/dc15986b-c1e7-464b-916d-dac02f7485e0" />
<img width="893" height="600" alt="2" src="https://github.com/user-attachments/assets/410ba6ab-4e82-46b7-b54a-b47d55ce6a39" />


---

# ✅ Key Takeaways

* Improved the Password Manager by replacing text files with structured JSON storage.
* Learned how to handle runtime errors using `try-except-else-finally`.
* Used `json.load()` to read existing data and `json.dump()` to save updated data.
* Added a **Search Password** feature for quick credential lookup.
* Prevented data loss by updating existing JSON records instead of overwriting them.
* Improved the application's reliability through proper exception handling and input validation.
* Practiced working with dictionaries, file handling and GUI programming together.

---

# 🚀 Practice Tasks

* ✏️ Add **Edit Password** functionality.
* 🗑️ Delete saved website credentials.
* 🔐 Encrypt passwords before saving them.
* 👁️ Add Show/Hide Password option.
* 📅 Store the date when each password is created.
* 📂 Export passwords to CSV.
* 🌙 Add Dark Mode support.

---

# 🎯 Day 30 Summary

Day 30 focused on making the Password Manager more practical and reliable by introducing **Error Handling**, **Exceptions**, and **JSON Data Storage**. Instead of storing passwords in plain text, the application now saves structured data in a JSON file, supports searching for saved credentials, and safely handles missing files using Python's exception handling mechanisms.

This project demonstrates how combining **Tkinter**, **JSON**, and **Exception Handling** can be used to build a more robust real-world desktop application.
