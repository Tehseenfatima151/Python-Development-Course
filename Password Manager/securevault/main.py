"""
main.py — entry point for SecureVault CLI Password Manager.

Usage:
    python main.py
"""

from app.password_manager import PasswordManager


def main() -> None:
    manager = PasswordManager()
    manager.run()


if __name__ == "__main__":
    main()
