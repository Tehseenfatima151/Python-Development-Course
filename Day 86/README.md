# Day 86 — Professional Portfolio Project: Password Manager (GUI)

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: Desktop Password Manager

A desktop GUI application built with **Tkinter** — generates strong random passwords, saves website/email/password entries to a local JSON file, and can search saved credentials by website. The app was actually launched on a virtual display and screenshotted (below) to confirm the UI renders correctly, and the core logic was tested independently of the GUI before writing this README.

---

## 🖼️ Verified Output
<img width="669" height="448" alt="image" src="https://github.com/user-attachments/assets/ba9a53fd-cecc-4128-9e3e-8dc6995a62b7" />


---

## 🧠 Concepts Covered

### 1. Separating logic from the GUI
The password generation, saving, and searching logic are written as **plain functions with no Tkinter code inside them** — the GUI functions call these, rather than mixing business logic directly into button callbacks.

```python
def generate_password(length_letters=10, length_symbols=3, length_numbers=3) -> str:
    letters = [random.choice(string.ascii_letters) for _ in range(length_letters)]
    symbols = [random.choice("!#$%&*+-_=?") for _ in range(length_symbols)]
    numbers = [random.choice(string.digits) for _ in range(length_numbers)]
    password_chars = letters + symbols + numbers
    random.shuffle(password_chars)
    return "".join(password_chars)
```
This separation means `generate_password()`, `save_entry()`, and `find_entry()` can be **tested directly in a terminal** without ever opening a window — exactly how this project was verified (see "Tested Output" below).

### 2. Persisting data with JSON
```python
def save_entry(website, email, password):
    data = load_data()
    data[website] = {"email": email, "password": password}
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)
```
Each website maps to a dictionary of its own — `json.dump(..., indent=4)` keeps the saved file human-readable, useful for debugging during development.

### 3. Handling a missing/corrupt data file gracefully
```python
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
```
On the very first run, `passwords.json` doesn't exist yet — catching `FileNotFoundError` (and `JSONDecodeError`, in case the file gets corrupted) lets the app start fresh instead of crashing.

### 4. Building a form layout with Tkinter's grid system
```python
website_label.grid(row=1, column=0, sticky="e", pady=6, padx=(0, 10))
website_entry.grid(row=1, column=1, sticky="w")
search_button.grid(row=1, column=2, padx=(8, 0))
```
`grid()` positions widgets in a table-like layout — `sticky="e"`/`"w"` aligns labels/entries to the east/west edge of their cell, keeping the form visually aligned like a real form rather than scattered widgets.

### 5. Confirmation dialogs before saving
```python
is_ok = messagebox.askokcancel(
    title=f"Save entry for {website}?",
    message=f"Website: {website}\nEmail: {email}\nPassword: {password}\n\nSave this entry?"
)
if is_ok:
    save_entry(website, email, password)
```
Showing the user exactly what will be saved — and requiring explicit confirmation — prevents accidental saves from a typo, especially for something as sensitive as a password entry.

### 6. Clipboard integration
```python
import pyperclip
pyperclip.copy(password)
```
Generated (and found) passwords are copied to the clipboard automatically, so the user can paste them directly into the real website's password field without retyping.

### 7. Case-insensitive search
```python
def find_entry(website):
    data = load_data()
    for saved_site, details in data.items():
        if saved_site.lower() == website.lower():
            return details
    return None
```
Comparing lowercased versions of both strings means searching `"GitHub.com"` still finds an entry saved as `"github.com"`.

---

## 📂 Project Structure
```
day85/
├── password_manager.py
├── screenshot.png
└── passwords.json     # auto-created on first save (not included — starts empty)
```

## ▶️ How to Run
```bash
pip install pyperclip
python password_manager.py
```
Tkinter ships with standard Python installs on Windows/Mac. On some Linux distributions it needs a separate install: `sudo apt install python3-tk`.

---

## 🧪 Tested Output
Core logic was run directly (outside the GUI) before this README was written:

```
=== Testing generate_password() ===
Generated password 1: !T0Z#gX_aDM02Dzs (length: 16)
Generated password 2: TSvX=yBSJ?TI014+ (length: 16)
Generated password 3: gCTbid?D3#e4rZ#5 (length: 16)

=== Testing save_entry() ===
Saved 2 entries.

=== Testing find_entry() — exact match ===
Found: {'email': 'tehseen@example.com', 'password': 'Tst!9284kLp'}

=== Testing find_entry() — case-insensitive match ===
Found (case-insensitive): {'email': 'tehseen@example.com', 'password': 'Tst!9284kLp'}

=== Testing find_entry() — not found ===
Not found result: None

✅ All core logic tests passed
```
The full GUI was then launched on a virtual display to confirm the window renders and lays out correctly — see the screenshot above.

---

## ✅ Key Takeaways
- Keeping business logic (password generation, file I/O, search) separate from GUI callback functions makes the app testable without ever opening a window — a habit worth carrying into any GUI or web project.
- `json.dump(..., indent=4)` is a small addition that makes a saved data file human-readable during development/debugging.
- Always handle the "first run, file doesn't exist yet" case explicitly — `FileNotFoundError` is expected, not exceptional, for any app that persists data to disk.
- A confirmation dialog before saving sensitive data is good UX — it costs one extra click but prevents accidental typos from being silently saved.
- Tkinter's `grid()` layout, used consistently with `sticky`/`padx`/`pady`, produces a genuinely clean form layout without needing a heavier GUI framework.

## 📝 Practice Tasks
1. Add real encryption (e.g. using the `cryptography` package's `Fernet`) instead of storing passwords in plain JSON.
2. Add a "Delete Entry" button that removes a saved website from `passwords.json`.
3. Add password strength validation — warn if a manually-typed password is too short or lacks variety.
4. Add a master password screen that must be entered correctly before the main window even opens.
