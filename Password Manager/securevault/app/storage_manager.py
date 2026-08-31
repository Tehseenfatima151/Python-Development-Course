"""
StorageManager — safe JSON-based CRUD for vault entries.

Storage format (vault.json):
{
    "entries": [
        {
            "id":         "<uuid>",
            "website":    "example.com",
            "username":   "user@example.com",
            "password":   "<fernet-token>",
            "created_at": "2024-01-01T12:00:00",
            "updated_at": "2024-01-01T12:00:00"
        },
        ...
    ]
}

Passwords are ALWAYS stored encrypted. Plaintext is never written to disk.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class StorageError(Exception):
    """Raised for storage-related failures."""


class StorageManager:
    """
    Handles all vault file operations:
      - Loading and saving entries.
      - Adding, searching, updating, and deleting credential records.
      - Atomic file writes to prevent corruption.
    """

    def __init__(self, vault_file: Path) -> None:
        """
        Args:
            vault_file: Path to the JSON file that stores encrypted entries.
        """
        self._vault_file = vault_file

    # ------------------------------------------------------------------
    # Load / Save
    # ------------------------------------------------------------------

    def load(self) -> dict:
        """
        Load and return the full vault data structure.

        Returns:
            A dict with an "entries" key containing a list of entry dicts.
            Returns an empty vault if the file does not exist yet.

        Raises:
            StorageError: If the file exists but cannot be read or parsed.
        """
        if not self._vault_file.exists():
            return {"entries": []}

        try:
            with open(self._vault_file, "r", encoding="utf-8") as fh:
                content = fh.read().strip()
                if not content:
                    return {"entries": []}
                data = json.loads(content)
                if "entries" not in data:
                    data["entries"] = []
                return data
        except json.JSONDecodeError as exc:
            raise StorageError("Vault data is corrupted and cannot be read.") from exc
        except PermissionError as exc:
            raise StorageError(f"Permission denied when reading vault: {exc}") from exc
        except OSError as exc:
            raise StorageError(f"Could not read vault file: {exc}") from exc

    def _save(self, data: dict) -> None:
        """
        Persist vault data atomically:
          1. Write to a temp file.
          2. Replace the original with the temp file.

        Raises:
            StorageError: If the write fails.
        """
        self._vault_file.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self._vault_file.with_suffix(".tmp")
        try:
            with open(tmp_path, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2, ensure_ascii=False)
            tmp_path.replace(self._vault_file)
        except PermissionError as exc:
            raise StorageError(f"Permission denied when writing vault: {exc}") from exc
        except OSError as exc:
            raise StorageError(f"Could not save vault file: {exc}") from exc
        finally:
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except OSError:
                    pass

    # ------------------------------------------------------------------
    # CRUD operations
    # ------------------------------------------------------------------

    def add_entry(self, website: str, username: str, encrypted_password: str) -> dict:
        """
        Add a new credential entry to the vault.

        Args:
            website:            The website/service name.
            username:           The account username or email.
            encrypted_password: The Fernet-encrypted password token.

        Returns:
            The newly created entry dict.

        Raises:
            StorageError: If the entry cannot be saved.
            ValueError:   If required fields are empty.
        """
        self._validate_fields(website=website, username=username, password=encrypted_password)

        now = _utc_now()
        entry = {
            "id": str(uuid.uuid4()),
            "website": website.strip(),
            "username": username.strip(),
            "password": encrypted_password,
            "created_at": now,
            "updated_at": now,
        }
        data = self.load()
        data["entries"].append(entry)
        self._save(data)
        return entry

    def search_entries(self, query: str) -> list[dict]:
        """
        Search for entries whose website contains the query string
        (case-insensitive).

        Args:
            query: Partial or full website name to search for.

        Returns:
            A list of matching entry dicts (may be empty).
        """
        data = self.load()
        q = query.strip().lower()
        return [e for e in data["entries"] if q in e.get("website", "").lower()]

    def get_all_entries(self) -> list[dict]:
        """Return all entries from the vault."""
        data = self.load()
        return data["entries"]

    def get_entry_by_id(self, entry_id: str) -> Optional[dict]:
        """
        Return the entry with the given ID, or None if not found.

        Args:
            entry_id: The UUID string of the entry.
        """
        data = self.load()
        for entry in data["entries"]:
            if entry.get("id") == entry_id:
                return entry
        return None

    def update_entry(
        self,
        entry_id: str,
        username: Optional[str] = None,
        encrypted_password: Optional[str] = None,
        website: Optional[str] = None,
    ) -> bool:
        """
        Update an existing entry.

        Only supplied fields are updated. At least one field must be given.

        Args:
            entry_id:           The UUID of the entry to update.
            username:           New username (optional).
            encrypted_password: New encrypted password token (optional).
            website:            New website (optional).

        Returns:
            True if the entry was found and updated, False if not found.

        Raises:
            StorageError: If the update cannot be persisted.
        """
        data = self.load()
        for entry in data["entries"]:
            if entry.get("id") == entry_id:
                if website is not None:
                    entry["website"] = website.strip()
                if username is not None:
                    entry["username"] = username.strip()
                if encrypted_password is not None:
                    entry["password"] = encrypted_password
                entry["updated_at"] = _utc_now()
                self._save(data)
                return True
        return False

    def delete_entry(self, entry_id: str) -> bool:
        """
        Remove an entry from the vault.

        Args:
            entry_id: The UUID of the entry to delete.

        Returns:
            True if the entry was found and deleted, False if not found.

        Raises:
            StorageError: If the deletion cannot be persisted.
        """
        data = self.load()
        original_count = len(data["entries"])
        data["entries"] = [e for e in data["entries"] if e.get("id") != entry_id]
        if len(data["entries"]) == original_count:
            return False
        self._save(data)
        return True

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_fields(**kwargs: str) -> None:
        """Raise ValueError if any supplied field is empty."""
        for field, value in kwargs.items():
            if not value or not value.strip():
                raise ValueError(f"Field '{field}' must not be empty.")


def _utc_now() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
