"""
PasswordManager — main application controller.

Orchestrates login, the interactive menu, and all vault operations.
Delegates to specialised managers for auth, encryption, storage,
clipboard, session tracking, and password generation.
"""

import getpass
import sys
from pathlib import Path
from typing import Optional

from app.auth_manager import AuthManager, AuthError, MAX_LOGIN_ATTEMPTS
from app.clipboard_manager import ClipboardManager, ClipboardError
from app.encryption_manager import EncryptionManager, EncryptionError
from app.password_generator import PasswordGenerator
from app.session_manager import SessionManager
from app.storage_manager import StorageManager, StorageError

# ------------------------------------------------------------------
# Configurable constants
# ------------------------------------------------------------------
SESSION_TIMEOUT = 300          # seconds (5 minutes)
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
AUTH_FILE = DATA_DIR / "auth.json"
VAULT_FILE = DATA_DIR / "vault.json"

# Menu option labels
MENU_OPTIONS = {
    "1": "Add Password",
    "2": "Search Password",
    "3": "View All Entries",
    "4": "Update Password",
    "5": "Delete Password",
    "6": "Logout",
    "7": "Exit",
}


class PasswordManager:
    """
    Top-level application controller for SecureVault.

    Handles:
      - First-time setup and subsequent login.
      - The main interactive menu loop.
      - Session timeout enforcement.
      - Delegation to specialised sub-managers.
    """

    def __init__(
        self,
        auth_file: Path = AUTH_FILE,
        vault_file: Path = VAULT_FILE,
        session_timeout: int = SESSION_TIMEOUT,
    ) -> None:
        self._auth = AuthManager(auth_file)
        self._enc = EncryptionManager()
        self._storage = StorageManager(vault_file)
        self._session = SessionManager(session_timeout)
        self._clipboard = ClipboardManager()
        self._generator = PasswordGenerator()

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the application loop."""
        _print_banner()
        while True:
            if not self._auth.is_initialised():
                if not self._first_time_setup():
                    _print_error("Setup failed. Exiting.")
                    sys.exit(1)
            if not self._login():
                _print_error("Too many failed attempts. Exiting.")
                sys.exit(1)
            # Main menu loop — returns when the user logs out
            keep_running = self._main_menu()
            if not keep_running:
                _print_info("Goodbye.")
                sys.exit(0)
            # User chose Logout — loop back to login

    # ------------------------------------------------------------------
    # First-time setup
    # ------------------------------------------------------------------

    def _first_time_setup(self) -> bool:
        """
        Prompt the user to create a master password on first launch.

        Returns:
            True if setup completed successfully, False otherwise.
        """
        print("\n  Welcome to SecureVault.")
        print("  Your vault is protected by a Master Password.\n")
        print("  No vault found. Let's set one up.\n")

        while True:
            pw = getpass.getpass("  Create Master Password: ")
            valid, errors = PasswordGenerator.validate_strength(pw)
            if not valid:
                print()
                for err in errors:
                    _print_error(err)
                print()
                continue

            confirm = getpass.getpass("  Confirm Master Password: ")
            if pw != confirm:
                _print_error("Passwords do not match. Please try again.")
                print()
                continue

            try:
                self._auth.setup(pw)
                _print_success("Master password set. Your vault is ready.")
                return True
            except AuthError as exc:
                _print_error(str(exc))
                return False
            finally:
                # Wipe local references
                pw = ""
                confirm = ""

    # ------------------------------------------------------------------
    # Login
    # ------------------------------------------------------------------

    def _login(self) -> bool:
        """
        Prompt for the master password and verify it.

        Returns:
            True if authentication succeeded, False after max attempts.
        """
        print()
        for attempt in range(1, MAX_LOGIN_ATTEMPTS + 1):
            pw = getpass.getpass("  Master Password: ")
            try:
                if self._auth.verify(pw):
                    enc_salt = self._auth.get_enc_salt()
                    self._enc.initialise(pw, enc_salt)
                    self._session.start()
                    _print_success("Authentication successful.")
                    return True
                else:
                    remaining = MAX_LOGIN_ATTEMPTS - attempt
                    if remaining > 0:
                        _print_error(
                            f"Invalid master password. {remaining} attempt(s) remaining."
                        )
                    else:
                        _print_error("Invalid master password.")
            except AuthError as exc:
                _print_error(str(exc))
                return False
            finally:
                pw = ""

        return False

    # ------------------------------------------------------------------
    # Main menu loop
    # ------------------------------------------------------------------

    def _main_menu(self) -> bool:
        """
        Display the menu and dispatch user choices.

        Returns:
            False if the user chose Exit (terminate the process).
            True  if the user chose Logout (return to login).
        """
        while True:
            # Check session timeout before every menu display
            if self._session.is_expired():
                self._logout(expired=True)
                return True  # Back to login

            _print_menu()
            choice = input("  Select an option: ").strip()
            print()

            # Reset activity timer on every valid interaction
            self._session.reset()

            if choice == "1":
                self._add_password()
            elif choice == "2":
                self._search_password()
            elif choice == "3":
                self._view_all_entries()
            elif choice == "4":
                self._update_password()
            elif choice == "5":
                self._delete_password()
            elif choice == "6":
                self._logout()
                return True
            elif choice == "7":
                self._exit()
                return False
            else:
                _print_error("Invalid option. Please choose 1–7.")

    # ------------------------------------------------------------------
    # Menu handlers
    # ------------------------------------------------------------------

    def _add_password(self) -> None:
        """Prompt the user for credentials, encrypt, and store them."""
        print("  --- Add Password ---\n")

        website = _prompt("  Website: ")
        if not website:
            _print_error("Website cannot be empty.")
            return

        username = _prompt("  Username / Email: ")
        if not username:
            _print_error("Username cannot be empty.")
            return

        # Offer to generate a password
        use_gen = _prompt("  Generate a secure password? (y/n): ").lower()
        if use_gen == "y":
            length_str = _prompt(f"  Password length (default {self._generator._length}): ")
            if length_str.isdigit():
                self._generator = PasswordGenerator(int(length_str))
            plaintext_pw = self._generator.generate()
            print("  Password generated.")
        else:
            plaintext_pw = getpass.getpass("  Password: ")
            if not plaintext_pw:
                _print_error("Password cannot be empty.")
                return

        try:
            encrypted_pw = self._enc.encrypt(plaintext_pw)
        except EncryptionError as exc:
            _print_error(str(exc))
            return
        finally:
            plaintext_pw = ""

        try:
            self._storage.add_entry(website, username, encrypted_pw)
            _print_success("Password saved successfully.")
        except (StorageError, ValueError) as exc:
            _print_error(str(exc))

    def _search_password(self) -> None:
        """Search for entries by website name and display results."""
        print("  --- Search Password ---\n")
        query = _prompt("  Enter website to search: ")
        if not query:
            _print_error("Search query cannot be empty.")
            return

        try:
            results = self._storage.search_entries(query)
        except StorageError as exc:
            _print_error(str(exc))
            return

        if not results:
            _print_info(f"No entries found for '{query}'.")
            return

        print(f"\n  Found {len(results)} entry/entries:\n")
        for i, entry in enumerate(results, 1):
            print(f"  [{i}] Website : {entry['website']}")
            print(f"      Username: {entry['username']}")
            print(f"      ID      : {entry['id']}")

            # Decrypt and optionally show / copy password
            try:
                decrypted = self._enc.decrypt(entry["password"])
            except EncryptionError as exc:
                _print_error(f"Could not decrypt entry {entry['id']}: {exc}")
                continue

            action = _prompt("\n  (v)iew password  (c)opy to clipboard  (s)kip: ").lower()
            if action == "v":
                print(f"\n  Password: {decrypted}\n")
            elif action == "c":
                self._copy_to_clipboard(decrypted)
            else:
                print()

            decrypted = ""  # Wipe from local scope

    def _view_all_entries(self) -> None:
        """Display all entries — website and username only, no passwords."""
        print("  --- All Entries ---\n")
        try:
            entries = self._storage.get_all_entries()
        except StorageError as exc:
            _print_error(str(exc))
            return

        if not entries:
            _print_info("No entries saved yet.")
            return

        for i, entry in enumerate(entries, 1):
            print(f"  {i:>3}. {entry['website']}  —  {entry['username']}")
            print(f"       ID: {entry['id']}")
        print()

    def _update_password(self) -> None:
        """Allow the user to update the username or password of an entry."""
        print("  --- Update Password ---\n")
        entry_id = _prompt("  Enter the Entry ID to update: ").strip()
        if not entry_id:
            _print_error("Entry ID cannot be empty.")
            return

        try:
            entry = self._storage.get_entry_by_id(entry_id)
        except StorageError as exc:
            _print_error(str(exc))
            return

        if not entry:
            _print_error("No entry found with that ID.")
            return

        print(f"\n  Updating: {entry['website']}  ({entry['username']})\n")
        print("  Leave a field blank to keep the current value.\n")

        new_username: Optional[str] = None
        new_enc_pw: Optional[str] = None

        username_input = _prompt("  New username (or press Enter to skip): ")
        if username_input.strip():
            new_username = username_input.strip()

        pw_choice = _prompt("  Update password? (y/n): ").lower()
        if pw_choice == "y":
            use_gen = _prompt("  Generate a secure password? (y/n): ").lower()
            if use_gen == "y":
                new_plain = self._generator.generate()
                print("  Password generated.")
            else:
                new_plain = getpass.getpass("  New Password: ")
                if not new_plain:
                    _print_error("Password cannot be empty.")
                    return
            try:
                new_enc_pw = self._enc.encrypt(new_plain)
            except EncryptionError as exc:
                _print_error(str(exc))
                return
            finally:
                new_plain = ""

        if new_username is None and new_enc_pw is None:
            _print_info("No changes made.")
            return

        try:
            updated = self._storage.update_entry(
                entry_id,
                username=new_username,
                encrypted_password=new_enc_pw,
            )
            if updated:
                _print_success("Entry updated successfully.")
            else:
                _print_error("Entry not found.")
        except StorageError as exc:
            _print_error(str(exc))

    def _delete_password(self) -> None:
        """Delete an entry after user confirmation."""
        print("  --- Delete Password ---\n")
        entry_id = _prompt("  Enter the Entry ID to delete: ").strip()
        if not entry_id:
            _print_error("Entry ID cannot be empty.")
            return

        try:
            entry = self._storage.get_entry_by_id(entry_id)
        except StorageError as exc:
            _print_error(str(exc))
            return

        if not entry:
            _print_error("No entry found with that ID.")
            return

        print(f"\n  Entry: {entry['website']}  ({entry['username']})\n")
        confirm = _prompt("  Are you sure you want to delete this entry? (y/n): ").lower()
        if confirm != "y":
            _print_info("Deletion cancelled.")
            return

        try:
            deleted = self._storage.delete_entry(entry_id)
            if deleted:
                _print_success("Entry deleted.")
            else:
                _print_error("Entry not found.")
        except StorageError as exc:
            _print_error(str(exc))

    # ------------------------------------------------------------------
    # Clipboard
    # ------------------------------------------------------------------

    def _copy_to_clipboard(self, secret: str) -> None:
        """Copy *secret* to the clipboard and notify the user."""
        try:
            self._clipboard.copy(secret)
            _print_success(
                f"Password copied to clipboard. "
                f"It will be cleared in {self._clipboard._clear_delay} seconds."
            )
        except ClipboardError as exc:
            _print_error(str(exc))

    # ------------------------------------------------------------------
    # Logout / Exit
    # ------------------------------------------------------------------

    def _logout(self, expired: bool = False) -> None:
        """Clear session state and encryption key."""
        self._enc.clear()
        self._session.end()
        self._clipboard.clear_now()
        if expired:
            print("\n  Session expired due to inactivity. Please login again.\n")
        else:
            _print_info("Logged out.")

    def _exit(self) -> None:
        """Perform a clean shutdown."""
        self._enc.clear()
        self._session.end()
        self._clipboard.clear_now()
        _print_info("Goodbye.")


# ------------------------------------------------------------------
# CLI helpers
# ------------------------------------------------------------------

def _print_banner() -> None:
    print("\n" + "=" * 42)
    print("   SECUREVAULT PASSWORD MANAGER")
    print("=" * 42 + "\n")


def _print_menu() -> None:
    print("\n" + "-" * 42)
    print("  SECUREVAULT PASSWORD MANAGER")
    print("-" * 42)
    for key, label in MENU_OPTIONS.items():
        print(f"  {key}. {label}")
    print("-" * 42)


def _print_success(msg: str) -> None:
    print(f"\n  [OK] {msg}\n")


def _print_error(msg: str) -> None:
    print(f"\n  [!] {msg}\n")


def _print_info(msg: str) -> None:
    print(f"\n  {msg}\n")


def _prompt(label: str) -> str:
    """Display *label* and return stripped user input."""
    try:
        return input(label).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return ""
