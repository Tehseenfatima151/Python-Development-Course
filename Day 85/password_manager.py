"""
Day 85 — Professional Portfolio Project: Password Manager (GUI)

A desktop password manager built with Tkinter — generates strong random
passwords, saves credentials locally in an encrypted-structure-ready JSON
file, and lets you search saved entries by website.

Run: python password_manager.py
"""

import json
import random
import string
import tkinter as tk
from tkinter import messagebox

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

DATA_FILE = "passwords.json"

# ---------------------------- Core Logic ---------------------------------
# Kept separate from the GUI functions below so they can be tested
# independently (see test_password_manager.py).

def generate_password(length_letters=10, length_symbols=3, length_numbers=3) -> str:
    """Generate a randomized, shuffled password from letters/symbols/numbers."""
    letters = [random.choice(string.ascii_letters) for _ in range(length_letters)]
    symbols = [random.choice("!#$%&*+-_=?") for _ in range(length_symbols)]
    numbers = [random.choice(string.digits) for _ in range(length_numbers)]

    password_chars = letters + symbols + numbers
    random.shuffle(password_chars)
    return "".join(password_chars)


def load_data() -> dict:
    """Load saved credentials from the JSON file. Returns {} if none exist."""
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_entry(website: str, email: str, password: str) -> dict:
    """Add/overwrite one entry and persist all data to the JSON file."""
    data = load_data()
    data[website] = {"email": email, "password": password}
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)
    return data


def find_entry(website: str) -> dict | None:
    """Look up a saved entry by website name (case-insensitive match)."""
    data = load_data()
    for saved_site, details in data.items():
        if saved_site.lower() == website.lower():
            return details
    return None


# ---------------------------- GUI Functions -------------------------------

def gui_generate_password():
    password = generate_password()
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    if CLIPBOARD_AVAILABLE:
        pyperclip.copy(password)


def gui_save():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not website or not email or not password:
        messagebox.showwarning("Missing Info", "Please don't leave any fields empty.")
        return

    is_ok = messagebox.askokcancel(
        title=f"Save entry for {website}?",
        message=f"Website: {website}\nEmail: {email}\nPassword: {password}\n\nSave this entry?"
    )
    if is_ok:
        save_entry(website, email, password)
        website_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        website_entry.focus()
        messagebox.showinfo("Saved", f"Credentials for '{website}' saved successfully.")


def gui_search():
    website = website_entry.get().strip()
    if not website:
        messagebox.showwarning("Missing Info", "Enter a website name to search for.")
        return

    result = find_entry(website)
    if result:
        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(result["password"])
        messagebox.showinfo(
            website,
            f"Email: {result['email']}\nPassword: {result['password']}"
            + ("\n\n(Password copied to clipboard)" if CLIPBOARD_AVAILABLE else "")
        )
    else:
        messagebox.showinfo("Not Found", f"No saved entry found for '{website}'.")


# ---------------------------- GUI Layout -----------------------------------

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Password Manager")
    window.config(padx=40, pady=40, bg="#1B2233")

    FONT_LABEL = ("JetBrains Mono", 11)
    FONT_ENTRY = ("Inter", 11)
    BG = "#1B2233"
    FG = "#E7EAF3"
    ACCENT = "#5EEAD4"

    # ---- Logo / Title ----
    title_label = tk.Label(window, text="🔐 Password Manager", font=("JetBrains Mono", 18, "bold"),
                            bg=BG, fg=ACCENT)
    title_label.grid(row=0, column=0, columnspan=3, pady=(0, 24))

    # ---- Website ----
    website_label = tk.Label(window, text="Website:", font=FONT_LABEL, bg=BG, fg=FG)
    website_label.grid(row=1, column=0, sticky="e", pady=6, padx=(0, 10))
    website_entry = tk.Entry(window, width=32, font=FONT_ENTRY)
    website_entry.grid(row=1, column=1, sticky="w")
    website_entry.focus()

    search_button = tk.Button(window, text="Search", command=gui_search,
                               bg=ACCENT, fg="#08141A", font=("Inter", 9, "bold"), relief="flat")
    search_button.grid(row=1, column=2, padx=(8, 0))

    # ---- Email ----
    email_label = tk.Label(window, text="Email/Username:", font=FONT_LABEL, bg=BG, fg=FG)
    email_label.grid(row=2, column=0, sticky="e", pady=6, padx=(0, 10))
    email_entry = tk.Entry(window, width=45, font=FONT_ENTRY)
    email_entry.grid(row=2, column=1, columnspan=2, sticky="w")
    email_entry.insert(0, "your.email@example.com")

    # ---- Password ----
    password_label = tk.Label(window, text="Password:", font=FONT_LABEL, bg=BG, fg=FG)
    password_label.grid(row=3, column=0, sticky="e", pady=6, padx=(0, 10))
    password_entry = tk.Entry(window, width=32, font=FONT_ENTRY)
    password_entry.grid(row=3, column=1, sticky="w")

    generate_button = tk.Button(window, text="Generate", command=gui_generate_password,
                                 bg="#FBBF24", fg="#08141A", font=("Inter", 9, "bold"), relief="flat")
    generate_button.grid(row=3, column=2, padx=(8, 0))

    # ---- Save ----
    add_button = tk.Button(window, text="Add / Save Entry", command=gui_save,
                            width=39, bg=ACCENT, fg="#08141A", font=("Inter", 10, "bold"), relief="flat")
    add_button.grid(row=4, column=1, columnspan=2, pady=(20, 0), sticky="w")

    window.mainloop()
