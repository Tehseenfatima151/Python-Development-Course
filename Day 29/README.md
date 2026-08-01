# Day 29 – Password Manager (Tkinter GUI)

## 📌 Overview

Day 29 mein humne Python ki **Tkinter GUI library** use karke ek **Password Manager Application** banai.

Is project ka main objective tha ek simple desktop application banana jo:

* Strong random passwords generate kare
* Password automatically clipboard mein copy kare
* Website, Email aur Password ko save kare
* User se confirmation lekar data file mein store kare

Is project ke through humne **GUI Development, Random Password Generation, File Handling, Message Boxes aur Clipboard Integration** ko practically implement kiya.

---

# 🔐 Project Features

* 🖥️ Tkinter GUI
* 🔑 Strong Random Password Generator
* 📋 Automatic Clipboard Copy
* 💾 Save Passwords in a Text File
* ⚠️ Input Validation
* ✅ Confirmation Dialog before Saving
* 🖼️ Logo using Canvas
* 📧 Default Email Address

---

# 📁 Project Structure

```text
password-manager/
│
├── main.py
├── logo.png
└── data.txt
```

| File       | Description            |
| ---------- | ---------------------- |
| `main.py`  | Main application logic |
| `logo.png` | Password Manager logo  |
| `data.txt` | Stores saved passwords |

---

# 🖥️ User Interface

The application consists of:

* Logo Image
* Website Entry
* Email / Username Entry
* Password Entry
* Generate Password Button
* Add Button

Simple and clean interface built using **Tkinter Grid Layout**.

---

# 🔑 Password Generator

The application automatically creates a **strong random password**.

Password contains:

* Uppercase Letters
* Lowercase Letters
* Numbers
* Symbols

Random functions used:

```python
choice()
randint()
shuffle()
```

### Process

```text
Letters
     +
Numbers
     +
Symbols
     ↓
Shuffle
     ↓
Strong Password
```

Generated password is automatically inserted into the Password field.

---

# 📋 Clipboard Support

The project uses the **pyperclip** package.

```python
pyperclip.copy(password)
```

As soon as a password is generated, it is automatically copied to the clipboard so the user can paste it anywhere using **Ctrl + V**.

---

# 💾 Saving Passwords

When the **Add** button is pressed:

* Website name is collected
* Email is collected
* Password is collected

Then a confirmation dialog appears.

If the user confirms, data is saved in **data.txt**.

Saved format:

```text
Website | Email | Password
```

Example:

```text
Google | shine@gmail.com | G#8dP2@Lm9
```

---

# ⚠️ Input Validation

Before saving, the application checks whether required fields are empty.

```python
if len(website) == 0 or len(password) == 0:
```

If any required field is empty, a message box is displayed asking the user to complete all fields.

This prevents incomplete records from being saved.

---

# 💬 Message Boxes

Tkinter's **messagebox** module is used.

### Information Dialog

```python
messagebox.showinfo()
```

Displays warning messages.

### Confirmation Dialog

```python
messagebox.askokcancel()
```

Asks the user whether the entered information should be saved.

---

# 📂 File Handling

Passwords are stored using append mode.

```python
with open("data.txt", "a") as file:
```

Append mode (`"a"`) adds new records without deleting previous data.

Each password is stored on a new line.

---

# 🎨 Tkinter Widgets Used

The application uses the following widgets:

| Widget       | Purpose                   |
| ------------ | ------------------------- |
| `Tk()`       | Main window               |
| `Canvas`     | Display logo image        |
| `Label`      | Show text labels          |
| `Entry`      | User input fields         |
| `Button`     | Generate and Save actions |
| `PhotoImage` | Display logo              |
| `messagebox` | Show dialogs              |

---

# ⚙️ Application Flow

```text
Open Application
       ↓
Enter Website
       ↓
Enter Email
       ↓
Generate Password
       ↓
Password Copied to Clipboard
       ↓
Click Add
       ↓
Confirmation Dialog
       ↓
Save in data.txt
```

---

# 🧠 Important Concepts Learned

* Tkinter GUI Development
* Grid Layout
* Labels
* Entry Widgets
* Buttons
* Canvas
* Images
* Random Module
* Password Generation
* List Comprehension
* File Handling
* Append Mode
* Clipboard Integration (`pyperclip`)
* Message Boxes
* Input Validation

---

# 📸 Screenshot

<img width="875" height="588" alt="2" src="https://github.com/user-attachments/assets/5f12c1f4-f4fe-405a-97bd-7aba0fd28557" />


---

# ✅ Key Takeaways

* Built a complete desktop Password Manager using **Tkinter**
* Generated secure random passwords using Python's `random` module
* Learned to combine letters, numbers and symbols into strong passwords
* Automatically copied generated passwords to the clipboard using `pyperclip`
* Saved user data permanently using file handling
* Used `messagebox` to improve user interaction
* Implemented input validation before saving data
* Practiced event-driven programming with Tkinter buttons

---

# 🚀 Practice Tasks

* 🔍 Add a **Search Password** feature.
* 🗑️ Add Delete Password functionality.
* ✏️ Allow editing existing passwords.
* 👁️ Add Show/Hide Password button.
* 📄 Save passwords in **JSON** format instead of a text file.
* 🔐 Encrypt passwords before saving.
* 🎨 Add Dark Mode support.

---

# 🎯 Day 29 Summary

Day 29 introduced us to building a practical **Password Manager** using Python and Tkinter. The project combined GUI programming, random password generation, clipboard operations, file handling, user validation and confirmation dialogs into one real-world desktop application.

This project demonstrates how Python can be used to create useful productivity tools while strengthening concepts of GUI development and data management.
