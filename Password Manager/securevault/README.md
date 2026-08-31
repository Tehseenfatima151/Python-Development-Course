# 🔐 SecureVault — CLI Password Manager

> **A secure, OOP-based command-line password manager built with Python, Fernet encryption, and PBKDF2-HMAC-SHA256.**

SecureVault helps users securely store and manage multiple website credentials without keeping passwords in plaintext.

Every stored password is encrypted using **Fernet symmetric encryption** before being written to disk. The encryption key is derived from the user's **Master Password** using PBKDF2-HMAC-SHA256 and is never stored.

---

## ✨ Features

| 🔹 Feature              | 📝 Description                                         |
| ----------------------- | ------------------------------------------------------ |
| 🔑 Master Password      | Strong master password protects the entire vault       |
| 🛡️ Password Hashing    | PBKDF2-HMAC-SHA256 with 600,000 iterations             |
| 🔐 Fernet Encryption    | Every stored password is encrypted at rest             |
| 🎲 Password Generator   | Cryptographically secure password generation           |
| ➕ Add Credentials       | Store website, username, and encrypted password        |
| 🔎 Search Credentials   | Case-insensitive partial website search                |
| 📋 View Entries         | View websites and usernames without exposing passwords |
| ✏️ Update Credentials   | Update username or password securely                   |
| 🗑️ Delete Credentials  | Delete entries with confirmation                       |
| 📎 Clipboard Support    | Copy decrypted passwords to clipboard                  |
| 🧹 Clipboard Auto-Clear | Clipboard automatically clears after 30 seconds        |
| ⏱️ Auto Logout          | Session expires after 5 minutes of inactivity          |
| 🚪 Manual Logout        | Securely return to the login screen                    |
| 💾 JSON Storage         | Local storage with atomic file writes                  |
| 🧱 OOP Architecture     | Clean separation of responsibilities                   |
| 🧪 Automated Testing    | Comprehensive `pytest` test suite                      |

---

## 🛠️ Tech Stack

### 💻 Core

* 🐍 **Python 3.11+**
* 🔐 **Cryptography**
* 🔑 **Fernet**
* 🛡️ **PBKDF2-HMAC-SHA256**
* 📄 **JSON**

### 📦 Python Libraries

* `cryptography` — encryption and secure key derivation
* `hashlib` — PBKDF2-HMAC-SHA256 hashing
* `getpass` — secure password input
* `secrets` — cryptographically secure random generation
* `pyperclip` — clipboard integration
* `json` — local data persistence
* `pathlib` / `os` — file handling
* `pytest` — automated testing

---

# 🏗️ Project Architecture

```text
securevault/
│
├── 🚀 main.py
├── 📦 requirements.txt
├── 📖 README.md
├── 🚫 .gitignore
│
├── 📁 app/
│   ├── __init__.py
│   ├── 🎛️ password_manager.py
│   ├── 🔑 auth_manager.py
│   ├── 🔐 encryption_manager.py
│   ├── 💾 storage_manager.py
│   ├── 🎲 password_generator.py
│   ├── 📋 clipboard_manager.py
│   └── ⏱️ session_manager.py
│
├── 📁 data/
│   └── .gitkeep
│
└── 🧪 tests/
    ├── __init__.py
    ├── test_auth.py
    ├── test_encryption.py
    ├── test_storage.py
    ├── test_password_generator.py
    └── test_session.py
```

> 🔒 `vault.json` and `auth.json` are generated at runtime and excluded from Git using `.gitignore`.

---

# 🧩 Module Responsibilities

### 🎛️ `PasswordManager`

Main application controller responsible for:

* First-time setup
* Login flow
* Interactive CLI menu
* Password operations
* Logout
* Session management

---

### 🔑 `AuthManager`

Responsible for Master Password authentication.

* Generates secure random salts
* Hashes the Master Password
* Stores only authentication data
* Verifies login attempts
* Uses constant-time comparison with `hmac.compare_digest`

---

### 🔐 `EncryptionManager`

Responsible for vault encryption.

* Derives encryption key using PBKDF2HMAC
* Uses a separate encryption salt
* Initializes Fernet
* Encrypts passwords
* Decrypts passwords when required
* Clears encryption state on logout

---

### 💾 `StorageManager`

Handles secure JSON persistence.

* Add entries
* Search entries
* Update entries
* Delete entries
* Read vault data
* Atomic JSON writes
* Handles missing/corrupted files gracefully

---

### 🎲 `PasswordGenerator`

Generates strong random passwords using Python's `secrets` module.

Generated passwords contain:

* 🔠 Uppercase letters
* 🔡 Lowercase letters
* 🔢 Numbers
* 🔣 Special characters

---

### 📋 `ClipboardManager`

Provides secure clipboard functionality.

* Copies passwords using `pyperclip`
* Avoids unnecessary password display
* Automatically clears clipboard after **30 seconds**

---

### ⏱️ `SessionManager`

Controls session security.

* Tracks last user activity
* Uses a **300-second timeout**
* Resets timer after user interaction
* Automatically expires inactive sessions

---

# 🔐 Security Architecture

SecureVault follows this security flow:

```text
              👤 Master Password
                      │
                      ▼
             🔑 PBKDF2-HMAC-SHA256
                      │
             ┌────────┴────────┐
             ▼                 ▼
        🔐 Auth Hash       🔐 Encryption Key
             │                 │
             ▼                 ▼
        auth.json          Fernet Encryption
                               │
                               ▼
                         💾 vault.json
                               │
                               ▼
                     🔒 Encrypted Passwords
```

### 🛡️ Security Principles

* 🔒 Master Password is **never stored in plaintext**
* 🔐 Vault passwords are encrypted before storage
* 🧂 Random salts are used
* 🔑 Encryption key is derived, not stored
* 🎲 `secrets` is used instead of the insecure `random` module
* 🕵️ Passwords are not unnecessarily displayed
* 📋 Clipboard automatically clears after 30 seconds
* ⏱️ Sessions expire after 5 minutes
* 🚫 Sensitive JSON files are excluded from Git
* 💾 Vault updates use atomic file replacement

---

# 📊 Password Storage Example

A stored vault entry looks conceptually like:

```json
{
  "id": "unique-id",
  "website": "github.com",
  "username": "user@example.com",
  "password": "gAAAAABm...encrypted-token...",
  "created_at": "2026-08-31T12:00:00",
  "updated_at": "2026-08-31T12:00:00"
}
```

🔒 Notice that the actual password is **never stored as plaintext**.

---

# 🚀 Installation

## 1️⃣ Clone the Repository

```bash
git clone <repository-url>
cd securevault
```

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 🪟 Windows

```bash
venv\Scripts\activate
```

### 🐧 Linux / macOS

```bash
source venv/bin/activate
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run SecureVault

Start the application:

```bash
python main.py
```

On the first launch:

1. 🔑 Create a Master Password
2. 🔐 Confirm the Master Password
3. 🗄️ SecureVault initializes the vault
4. 🚀 Access the password manager

On subsequent launches, you will be asked to authenticate using your Master Password.

---

# 🖥️ Application Menu

After successful authentication:

```text
========================================
        🔐 SECUREVAULT
      PASSWORD MANAGER
========================================

1. ➕ Add Password
2. 🔎 Search Password
3. 📋 View All Entries
4. ✏️ Update Password
5. 🗑️ Delete Password
6. 🚪 Logout
7. ❌ Exit

Select an option:
```

---

# 🧪 Testing

SecureVault includes a comprehensive automated test suite.

Run:

```bash
pytest -v
```

### ✅ Test Coverage

```text
Authentication Tests       → 20 tests
Encryption Tests           → 21 tests
Storage Tests              → 33 tests
Password Generator Tests   → 19 tests
Session Tests              → 13 tests
-----------------------------------------
Total                      → 103 tests
```

### 🏆 Test Result

```text
=============================
      SECUREVAULT TESTS
=============================

        103 PASSED ✅
        0 FAILED ❌
```

**103/103 tests passed successfully on Python 3.14.3.**

---

# 📋 Clipboard Security

When a password is copied:

```text
🔓 Password decrypted temporarily
             ↓
📋 Copied to clipboard
             ↓
⏳ 30 seconds
             ↓
🧹 Clipboard automatically cleared
```

This reduces the amount of time a sensitive password remains available in the clipboard.

---

# ⏱️ Session Security

SecureVault automatically logs the user out after:

**5 minutes = 300 seconds**

of inactivity.

```text
👤 User Login
      ↓
⏱️ Session Started
      ↓
💻 User Activity
      ↓
🔄 Timer Reset
      ↓
💤 5 Minutes Inactive
      ↓
🚪 Automatic Logout
```

---

# 📁 Data Security

The following files are generated locally:

```text
data/
├── vault.json 🔒
└── auth.json  🔑
```

These files are intentionally excluded from Git:

```gitignore
data/vault.json
data/auth.json
```

⚠️ **Never commit real credentials or vault files to GitHub.**

---

# 🧠 OOP Concepts Demonstrated

This project was designed to demonstrate practical Object-Oriented Programming concepts:

* 🧱 Classes and Objects
* 🔐 Encapsulation
* 🎯 Single Responsibility Principle
* 🔗 Composition
* 📦 Modular Architecture
* 🔄 Separation of Concerns
* 🧪 Testable Components
* 🛡️ Secure Resource Management

Each major responsibility is isolated into its own class, making the project easier to maintain, test, and extend.

---

# 🔮 Future Improvements

Possible future enhancements include:

* 🌐 GUI version
* 🗄️ SQLite encrypted database
* 🔐 Argon2-based password hashing
* 🔄 Password breach checking
* 📱 QR-code based credential sharing
* 👤 Multiple user profiles
* 🔑 Two-factor authentication
* 📊 Password strength dashboard
* 🔄 Vault backup and restore
* 🧩 Browser extension integration

---
# 🔮 Screenshoots
<img width="1197" height="729" alt="p1" src="https://github.com/user-attachments/assets/250e92ea-104f-4bcb-808c-7adc4b11edfe" />
<img width="1197" height="729" alt="p1" src="https://github.com/user-attachments/assets/dd5f6318-61bc-46a6-b202-186e305c9963" />
<img width="1200" height="727" alt="p3" src="https://github.com/user-attachments/assets/8975c037-2389-46ef-85eb-41d0e7e89a67" />

<img width="1191" height="728" alt="p4" src="https://github.com/user-attachments/assets/7009d2f5-3dc4-4657-b3a0-0309f604c6e3" />


---

# ⚠️ Security Disclaimer

SecureVault is an **educational project** designed to demonstrate secure Python development, OOP, cryptography, authentication, and local data management.

Although the project follows several security best practices, it should **not be considered a replacement for professionally audited password-management software**.

For production use, additional security hardening and professional security review would be recommended.

---

# 👩‍💻 Author

**Tehseen Fatima**

🎓 Software Engineering Student
💻 Full-Stack Developer
🤖 AI Enthusiast

---

# ⭐ Project Highlights

```text
🔐 Secure Master Password Authentication
🛡️ PBKDF2-HMAC-SHA256
🔒 Fernet Symmetric Encryption
🎲 Cryptographically Secure Password Generator
📋 Clipboard Auto-Clear
⏱️ 5-Minute Auto Logout
💾 Atomic JSON Storage
🧱 Object-Oriented Architecture
🧪 103 Automated Tests
✅ 103/103 Tests Passed
```

---

## ⭐ If You Find This Project Useful

Give the repository a ⭐ on GitHub and feel free to explore, improve, and contribute to the project.

**Built with Python 🐍 | Secured with Cryptography 🔐 | Tested with Pytest 🧪**
