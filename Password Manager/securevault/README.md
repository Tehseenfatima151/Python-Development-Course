# SecureVault — CLI Password Manager

## Overview

Managing dozens of unique, strong passwords is impractical without tooling.
SecureVault is a command-line password manager that lets you store, search, and
manage credentials locally. Every password is encrypted with Fernet symmetric
encryption before it touches disk; the encryption key is derived from your
Master Password using PBKDF2-HMAC-SHA256 and is never stored anywhere.

---

## Features

| Feature | Description |
|---|---|
| Master Password authentication | One strong password protects the entire vault |
| PBKDF2-HMAC-SHA256 hashing | Master Password never stored in plaintext |
| Fernet encryption | Every stored password is encrypted at rest |
| Secure password generator | Cryptographically secure passwords via `secrets` |
| Add credentials | Website, username, encrypted password |
| Search credentials | Case-insensitive partial website search |
| View all entries | Website and username only — passwords stay hidden |
| Update credentials | Change username or password for any entry |
| Delete credentials | Confirmation required before removal |
| Clipboard integration | Copy decrypted password; auto-clear after 30 s |
| Auto logout | Session expires after 5 minutes of inactivity |
| Manual logout | Returns to login screen without closing the app |
| JSON local storage | Atomic file writes, corruption-safe |
| OOP architecture | Clean separation of concerns across 7 modules |
| Automated tests | `pytest` test suite covering all core modules |

---

## Tech Stack

- **Python 3.11+**
- **cryptography** — Fernet encryption, PBKDF2HMAC key derivation
- **hashlib** — PBKDF2-HMAC-SHA256 for master password verification
- **getpass** — Secure password input (no echo)
- **secrets** — Cryptographically secure random generation
- **pyperclip** — Cross-platform clipboard access
- **json / pathlib / os** — Local storage and file handling
- **pytest** — Automated testing

---

## Project Architecture

```
securevault/
├── main.py                     Entry point
├── requirements.txt
├── README.md
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── password_manager.py     Main controller — menu, login, orchestration
│   ├── auth_manager.py         Master password setup, hashing, verification
│   ├── encryption_manager.py   PBKDF2 key derivation, Fernet encrypt/decrypt
│   ├── storage_manager.py      JSON CRUD — add, search, update, delete entries
│   ├── password_generator.py   Secure random password generation + validation
│   ├── clipboard_manager.py    Clipboard copy with auto-clear
│   └── session_manager.py      Inactivity timeout tracking
├── data/
│   ├── .gitkeep
│   ├── vault.json              (gitignored — created at runtime)
│   └── auth.json               (gitignored — created at runtime)
└── tests/
    ├── __init__.py
    ├── test_auth.py
    ├── test_encryption.py
    ├── test_storage.py
    ├── test_password_generator.py
    └── test_session.py
```

### Module responsibilities

**`PasswordManager`** (`password_manager.py`)
Orchestrates the entire application. Handles first-time setup, login flow,
the interactive menu loop, and delegates every operation to the appropriate
sub-manager. Enforces the session timeout before each menu cycle.

**`AuthManager`** (`auth_manager.py`)
Generates a random `auth_salt` and an `enc_salt` during setup. Hashes the
Master Password with PBKDF2-HMAC-SHA256 + `auth_salt` and persists only the
hash and both salts to `auth.json`. Performs constant-time hash comparison on
login via `hmac.compare_digest`.

**`EncryptionManager`** (`encryption_manager.py`)
Derives a 32-byte key from the Master Password using PBKDF2HMAC with the
stored `enc_salt`, base64url-encodes it, and initialises a `Fernet` instance.
`encrypt()` and `decrypt()` wrap Fernet; `clear()` destroys the key on logout.

**`StorageManager`** (`storage_manager.py`)
Reads and writes `vault.json`. All writes are atomic (write-to-temp then
replace). Handles missing files, empty files, and invalid JSON gracefully.

**`PasswordGenerator`** (`password_generator.py`)
Uses `secrets.choice` to build passwords that are guaranteed to contain at
least one uppercase letter, one lowercase letter, one digit, and one special
character. Also validates password strength for user-supplied passwords.

**`ClipboardManager`** (`clipboard_manager.py`)
Copies secrets to the clipboard via `pyperclip` and schedules a daemon thread
to overwrite the clipboard with an empty string after 30 seconds.

**`SessionManager`** (`session_manager.py`)
Records the timestamp of the last user action. `is_expired()` returns `True`
once `SESSION_TIMEOUT` (300 s) has elapsed. Calling `reset()` after each menu
interaction keeps active sessions alive.

---

## Installation

```bash
git clone <repository-url>
cd securevault
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

> **Linux clipboard note:** `pyperclip` requires `xclip` or `xsel`.
> Install with: `sudo apt install xclip`

---

## Run

```bash
python main.py
```

On first launch you will be asked to create a Master Password. On subsequent
launches you will be prompted to authenticate.

---

## Testing

```bash
pytest -v
```

All tests use temporary directories (`tmp_path` fixture) and do not touch the
real `data/` files.

---

## Security Notes

- **Master Password is never stored in plaintext.** Only a PBKDF2-HMAC-SHA256
  hash (600 000 iterations) alongside a random salt is persisted.
- **Vault passwords are always encrypted.** `vault.json` contains only Fernet
  tokens; plaintext passwords exist only in memory and only while needed.
- **The encryption key is derived, not stored.** The Fernet key is re-derived
  from the Master Password on every login and discarded on logout.
- **Sensitive files are excluded from Git.** `data/vault.json` and
  `data/auth.json` are listed in `.gitignore`.
- **Clipboard is auto-cleared** 30 seconds after a password is copied.
- **Session expires** after 5 minutes of inactivity.
- **This project is for educational purposes.** It demonstrates secure
  Python coding practices. Before using it to protect real production
  credentials, have the implementation reviewed by a professional security
  engineer and consider additional hardening (e.g., file-system permissions,
  memory locking, audit logging).
