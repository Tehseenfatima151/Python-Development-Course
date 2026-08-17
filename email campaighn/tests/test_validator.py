"""Unit tests for ContactValidator and email format validation."""

import tempfile
import unittest
from pathlib import Path

from src.validator import ContactValidator


class TestContactValidator(unittest.TestCase):
    """Test suite for CSV loading, email validation, and deduplication."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _write_csv(self, filename: str, content: str) -> Path:
        p = self.temp_path / filename
        p.write_text(content, encoding="utf-8")
        return p

    def test_email_regex_valid_cases(self) -> None:
        valid_emails = [
            "ali@example.com",
            "sara.connor@sub.domain.org",
            "first.last+label@company.co.uk",
            "user123_456@domain.io",
        ]
        for em in valid_emails:
            self.assertTrue(ContactValidator.is_valid_email(em), f"Failed for {em}")

    def test_email_regex_invalid_cases(self) -> None:
        invalid_emails = [
            "plainaddress",
            "@missingusername.com",
            "username@.com",
            "user@domain",
            "user with spaces@domain.com",
            "",
            "   ",
            None,
        ]
        for em in invalid_emails:
            self.assertFalse(ContactValidator.is_valid_email(em), f"Should fail for {em}")

    def test_valid_csv_parsing(self) -> None:
        csv_file = self._write_csv(
            "valid.csv",
            "name,email\nAli,ali@example.com\nSara,sara@example.com\n",
        )
        validator = ContactValidator(csv_file)
        df, report = validator.validate()

        self.assertEqual(report.total_rows, 2)
        self.assertEqual(report.valid_count, 2)
        self.assertEqual(report.invalid_count, 0)
        self.assertEqual(len(df), 2)
        self.assertEqual(report.valid_contacts[0].name, "Ali")
        self.assertEqual(report.valid_contacts[0].email, "ali@example.com")

    def test_missing_required_columns(self) -> None:
        csv_file = self._write_csv("bad_columns.csv", "first_name,contact_email\nAli,ali@example.com\n")
        validator = ContactValidator(csv_file)
        with self.assertRaises(ValueError) as ctx:
            validator.validate()
        self.assertIn("missing required columns", str(ctx.exception).lower())

    def test_duplicate_email_handling(self) -> None:
        csv_file = self._write_csv(
            "duplicates.csv",
            "name,email\nAli,ali@example.com\nAli Duplicate,ali@example.com\nSara,sara@example.com\n",
        )
        validator = ContactValidator(csv_file)
        df, report = validator.validate()

        self.assertEqual(report.total_rows, 3)
        self.assertEqual(report.valid_count, 2)
        self.assertEqual(report.invalid_count, 1)
        self.assertIn("Duplicate", report.invalid_contacts[0].error_reason)

    def test_empty_rows_and_invalid_emails(self) -> None:
        csv_file = self._write_csv(
            "mixed.csv",
            "name,email\n"
            ",emptyname@example.com\n"
            "Valid User,user@example.com\n"
            "Bad Email,invalid-email-address\n"
            "No Email,\n",
        )
        validator = ContactValidator(csv_file)
        df, report = validator.validate()

        self.assertEqual(report.total_rows, 4)
        self.assertEqual(report.valid_count, 1)
        self.assertEqual(report.invalid_count, 3)
        self.assertEqual(report.valid_contacts[0].name, "Valid User")

    def test_file_not_found(self) -> None:
        validator = ContactValidator(self.temp_path / "non_existent.csv")
        with self.assertRaises(FileNotFoundError):
            validator.validate()


if __name__ == "__main__":
    unittest.main()
