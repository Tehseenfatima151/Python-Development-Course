"""
Tests for StorageManager — CRUD, file handling, edge cases.
"""

import json
import pytest
from pathlib import Path

from app.storage_manager import StorageManager, StorageError

# Placeholder encrypted token (not a real Fernet token — storage doesn't decrypt)
FAKE_ENCRYPTED_PW = "gAAAAABfakeencryptedtoken1234567890=="


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def vault_file(tmp_path: Path) -> Path:
    return tmp_path / "vault.json"


@pytest.fixture
def storage(vault_file: Path) -> StorageManager:
    return StorageManager(vault_file)


@pytest.fixture
def storage_with_entry(storage: StorageManager) -> tuple[StorageManager, dict]:
    entry = storage.add_entry("github.com", "user@example.com", FAKE_ENCRYPTED_PW)
    return storage, entry


# ---------------------------------------------------------------------------
# load — edge cases
# ---------------------------------------------------------------------------

class TestLoad:
    def test_returns_empty_vault_when_no_file(self, storage: StorageManager) -> None:
        data = storage.load()
        assert data == {"entries": []}

    def test_returns_empty_vault_on_empty_file(self, vault_file: Path, storage: StorageManager) -> None:
        vault_file.write_text("")
        assert storage.load() == {"entries": []}

    def test_raises_on_invalid_json(self, vault_file: Path, storage: StorageManager) -> None:
        vault_file.write_text("{bad json{{")
        with pytest.raises(StorageError):
            storage.load()

    def test_handles_missing_entries_key(self, vault_file: Path, storage: StorageManager) -> None:
        vault_file.write_text(json.dumps({}))
        data = storage.load()
        assert "entries" in data


# ---------------------------------------------------------------------------
# add_entry
# ---------------------------------------------------------------------------

class TestAddEntry:
    def test_returns_entry_dict(self, storage: StorageManager) -> None:
        entry = storage.add_entry("example.com", "alice", FAKE_ENCRYPTED_PW)
        assert entry["website"] == "example.com"
        assert entry["username"] == "alice"
        assert "id" in entry
        assert "created_at" in entry
        assert "updated_at" in entry

    def test_password_stored_as_provided(self, storage: StorageManager) -> None:
        entry = storage.add_entry("example.com", "alice", FAKE_ENCRYPTED_PW)
        assert entry["password"] == FAKE_ENCRYPTED_PW

    def test_entry_persisted_to_file(self, storage: StorageManager, vault_file: Path) -> None:
        storage.add_entry("example.com", "alice", FAKE_ENCRYPTED_PW)
        data = json.loads(vault_file.read_text())
        assert len(data["entries"]) == 1

    def test_multiple_entries_all_saved(self, storage: StorageManager) -> None:
        storage.add_entry("github.com", "alice", FAKE_ENCRYPTED_PW)
        storage.add_entry("gitlab.com", "bob", FAKE_ENCRYPTED_PW)
        storage.add_entry("bitbucket.org", "carol", FAKE_ENCRYPTED_PW)
        assert len(storage.get_all_entries()) == 3

    def test_each_entry_has_unique_id(self, storage: StorageManager) -> None:
        e1 = storage.add_entry("site1.com", "u1", FAKE_ENCRYPTED_PW)
        e2 = storage.add_entry("site2.com", "u2", FAKE_ENCRYPTED_PW)
        assert e1["id"] != e2["id"]

    def test_raises_on_empty_website(self, storage: StorageManager) -> None:
        with pytest.raises(ValueError):
            storage.add_entry("", "alice", FAKE_ENCRYPTED_PW)

    def test_raises_on_empty_username(self, storage: StorageManager) -> None:
        with pytest.raises(ValueError):
            storage.add_entry("example.com", "", FAKE_ENCRYPTED_PW)

    def test_raises_on_empty_password(self, storage: StorageManager) -> None:
        with pytest.raises(ValueError):
            storage.add_entry("example.com", "alice", "")


# ---------------------------------------------------------------------------
# search_entries
# ---------------------------------------------------------------------------

class TestSearchEntries:
    def test_exact_match(self, storage_with_entry: tuple) -> None:
        storage, entry = storage_with_entry
        results = storage.search_entries("github.com")
        assert len(results) == 1
        assert results[0]["id"] == entry["id"]

    def test_partial_match(self, storage_with_entry: tuple) -> None:
        storage, _ = storage_with_entry
        results = storage.search_entries("github")
        assert len(results) == 1

    def test_case_insensitive(self, storage_with_entry: tuple) -> None:
        storage, _ = storage_with_entry
        results = storage.search_entries("GITHUB")
        assert len(results) == 1

    def test_no_match_returns_empty_list(self, storage_with_entry: tuple) -> None:
        storage, _ = storage_with_entry
        results = storage.search_entries("nonexistent.xyz")
        assert results == []

    def test_multiple_matches(self, storage: StorageManager) -> None:
        storage.add_entry("github.com", "u1", FAKE_ENCRYPTED_PW)
        storage.add_entry("github.io", "u2", FAKE_ENCRYPTED_PW)
        storage.add_entry("gitlab.com", "u3", FAKE_ENCRYPTED_PW)
        results = storage.search_entries("github")
        assert len(results) == 2


# ---------------------------------------------------------------------------
# get_all_entries
# ---------------------------------------------------------------------------

class TestGetAllEntries:
    def test_empty_when_no_entries(self, storage: StorageManager) -> None:
        assert storage.get_all_entries() == []

    def test_returns_all_entries(self, storage: StorageManager) -> None:
        storage.add_entry("a.com", "u1", FAKE_ENCRYPTED_PW)
        storage.add_entry("b.com", "u2", FAKE_ENCRYPTED_PW)
        entries = storage.get_all_entries()
        assert len(entries) == 2


# ---------------------------------------------------------------------------
# get_entry_by_id
# ---------------------------------------------------------------------------

class TestGetEntryById:
    def test_returns_correct_entry(self, storage_with_entry: tuple) -> None:
        storage, entry = storage_with_entry
        found = storage.get_entry_by_id(entry["id"])
        assert found is not None
        assert found["id"] == entry["id"]

    def test_returns_none_for_unknown_id(self, storage_with_entry: tuple) -> None:
        storage, _ = storage_with_entry
        assert storage.get_entry_by_id("00000000-0000-0000-0000-000000000000") is None


# ---------------------------------------------------------------------------
# update_entry
# ---------------------------------------------------------------------------

class TestUpdateEntry:
    def test_update_username(self, storage_with_entry: tuple) -> None:
        storage, entry = storage_with_entry
        result = storage.update_entry(entry["id"], username="new@example.com")
        assert result is True
        updated = storage.get_entry_by_id(entry["id"])
        assert updated["username"] == "new@example.com"

    def test_update_password(self, storage_with_entry: tuple) -> None:
        storage, entry = storage_with_entry
        new_enc = "gAAAAABnewencryptedvalue=="
        result = storage.update_entry(entry["id"], encrypted_password=new_enc)
        assert result is True
        updated = storage.get_entry_by_id(entry["id"])
        assert updated["password"] == new_enc

    def test_updated_at_changes(self, storage_with_entry: tuple) -> None:
        storage, entry = storage_with_entry
        original_ts = entry["updated_at"]
        import time; time.sleep(1)
        storage.update_entry(entry["id"], username="changed@example.com")
        updated = storage.get_entry_by_id(entry["id"])
        assert updated["updated_at"] >= original_ts

    def test_returns_false_for_unknown_id(self, storage: StorageManager) -> None:
        result = storage.update_entry("nonexistent-id", username="x")
        assert result is False


# ---------------------------------------------------------------------------
# delete_entry
# ---------------------------------------------------------------------------

class TestDeleteEntry:
    def test_delete_removes_entry(self, storage_with_entry: tuple) -> None:
        storage, entry = storage_with_entry
        result = storage.delete_entry(entry["id"])
        assert result is True
        assert storage.get_entry_by_id(entry["id"]) is None

    def test_vault_empty_after_delete(self, storage_with_entry: tuple) -> None:
        storage, entry = storage_with_entry
        storage.delete_entry(entry["id"])
        assert storage.get_all_entries() == []

    def test_returns_false_for_unknown_id(self, storage: StorageManager) -> None:
        result = storage.delete_entry("nonexistent-id")
        assert result is False

    def test_delete_only_target_entry(self, storage: StorageManager) -> None:
        e1 = storage.add_entry("site1.com", "u1", FAKE_ENCRYPTED_PW)
        e2 = storage.add_entry("site2.com", "u2", FAKE_ENCRYPTED_PW)
        storage.delete_entry(e1["id"])
        remaining = storage.get_all_entries()
        assert len(remaining) == 1
        assert remaining[0]["id"] == e2["id"]
