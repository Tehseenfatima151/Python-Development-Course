"""Contact CSV and email format validator.

Loads contact data from CSV via Pandas, enforces schema requirements, validates
email addresses using standard RFC 5322 regex, detects internal duplicates, and
safely separates valid contacts from invalid ones with detailed reasons.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import pandas as pd

# RFC 5322 compliant simplified email validation regex
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
)


@dataclass
class ContactRecord:
    """Individual contact record with validation metadata."""

    row_index: int
    name: str
    email: str
    is_valid: bool
    error_reason: Optional[str] = None
    extra_fields: Optional[dict[str, str]] = None


@dataclass
class ValidationReport:
    """Aggregated validation statistics and contact records."""

    total_rows: int
    valid_count: int
    invalid_count: int
    valid_contacts: list[ContactRecord]
    invalid_contacts: list[ContactRecord]
    errors: list[str]

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0 or self.invalid_count > 0


class ContactValidator:
    """Validator for contact CSV files and email formats."""

    REQUIRED_COLUMNS = {"name", "email"}

    def __init__(self, csv_path: Path | str) -> None:
        self.csv_path = Path(csv_path)

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Check if an email address matches valid standard email format."""
        if not isinstance(email, str):
            return False
        cleaned = email.strip()
        if not cleaned or len(cleaned) > 254:
            return False
        return bool(EMAIL_REGEX.match(cleaned))

    def validate(self) -> tuple[pd.DataFrame, ValidationReport]:
        """Validate the CSV file and return clean DataFrame and validation report.

        Raises:
            FileNotFoundError: If the CSV file does not exist.
            ValueError: If the CSV file is empty or missing required columns.
        """
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Contacts file not found at: {self.csv_path}")

        try:
            # Read CSV with pandas, treating empty strings/whitespace as NaN
            df = pd.read_csv(self.csv_path, skipinitialspace=True, dtype=str)
        except pd.errors.EmptyDataError:
            raise ValueError(f"Contacts CSV file is completely empty: {self.csv_path}")
        except Exception as e:
            raise ValueError(f"Failed to parse CSV file ({self.csv_path}): {e}")

        # Normalize column names: lowercase and stripped
        df.columns = [str(c).strip().lower() for c in df.columns]

        missing_cols = self.REQUIRED_COLUMNS - set(df.columns)
        if missing_cols:
            raise ValueError(
                f"Contacts CSV is missing required columns: {', '.join(sorted(missing_cols))}. "
                f"Found columns: {', '.join(df.columns)}"
            )

        if df.empty:
            report = ValidationReport(
                total_rows=0,
                valid_count=0,
                invalid_count=0,
                valid_contacts=[],
                invalid_contacts=[],
                errors=["CSV file contains headers but no data rows."],
            )
            return pd.DataFrame(columns=["name", "email"]), report

        valid_records: list[ContactRecord] = []
        invalid_records: list[ContactRecord] = []
        seen_emails: set[str] = set()
        general_errors: list[str] = []

        valid_rows: list[dict] = []

        for idx, row in df.iterrows():
            row_num = idx + 2  # 1-indexed accounting for CSV header row

            raw_name = row.get("name")
            raw_email = row.get("email")

            # Extract any extra columns for advanced placeholder replacement
            extra_data = {
                k: str(v).strip()
                for k, v in row.items()
                if k not in ("name", "email") and pd.notna(v)
            }

            # 1. Validate Name
            if pd.isna(raw_name) or not str(raw_name).strip():
                inv = ContactRecord(
                    row_index=row_num,
                    name=str(raw_name) if pd.notna(raw_name) else "",
                    email=str(raw_email) if pd.notna(raw_email) else "",
                    is_valid=False,
                    error_reason=f"Row {row_num}: Name is missing or empty.",
                )
                invalid_records.append(inv)
                continue

            # 2. Validate Email
            if pd.isna(raw_email) or not str(raw_email).strip():
                inv = ContactRecord(
                    row_index=row_num,
                    name=str(raw_name).strip(),
                    email="",
                    is_valid=False,
                    error_reason=f"Row {row_num}: Email address is missing or empty.",
                )
                invalid_records.append(inv)
                continue

            name = str(raw_name).strip()
            email = str(raw_email).strip()
            email_lower = email.lower()

            # 3. Validate Email Format
            if not self.is_valid_email(email):
                inv = ContactRecord(
                    row_index=row_num,
                    name=name,
                    email=email,
                    is_valid=False,
                    error_reason=f"Row {row_num}: Invalid email syntax '{email}'.",
                )
                invalid_records.append(inv)
                continue

            # 4. Duplicate Check
            if email_lower in seen_emails:
                inv = ContactRecord(
                    row_index=row_num,
                    name=name,
                    email=email,
                    is_valid=False,
                    error_reason=f"Row {row_num}: Duplicate email address '{email}' (already processed in this CSV).",
                )
                invalid_records.append(inv)
                continue

            seen_emails.add(email_lower)
            rec = ContactRecord(
                row_index=row_num,
                name=name,
                email=email,
                is_valid=True,
                extra_fields=extra_data,
            )
            valid_records.append(rec)
            valid_rows.append({"name": name, "email": email, **extra_data})

        clean_df = pd.DataFrame(valid_rows) if valid_rows else pd.DataFrame(columns=["name", "email"])

        report = ValidationReport(
            total_rows=len(df),
            valid_count=len(valid_records),
            invalid_count=len(invalid_records),
            valid_contacts=valid_records,
            invalid_contacts=invalid_records,
            errors=general_errors,
        )

        return clean_df, report
