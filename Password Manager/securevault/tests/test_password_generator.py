"""
Tests for PasswordGenerator — secure password generation and strength validation.
"""

import string
import pytest

from app.password_generator import PasswordGenerator, MIN_LENGTH, MAX_LENGTH


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def gen() -> PasswordGenerator:
    return PasswordGenerator(length=16)


# ---------------------------------------------------------------------------
# generate — output properties
# ---------------------------------------------------------------------------

class TestGenerate:
    def test_returns_string(self, gen: PasswordGenerator) -> None:
        pw = gen.generate()
        assert isinstance(pw, str)

    def test_correct_default_length(self, gen: PasswordGenerator) -> None:
        pw = gen.generate()
        assert len(pw) == 16

    def test_custom_length(self) -> None:
        gen = PasswordGenerator(length=24)
        assert len(gen.generate()) == 24

    def test_length_clamped_to_minimum(self) -> None:
        gen = PasswordGenerator(length=2)   # Below MIN_LENGTH
        assert len(gen.generate()) >= MIN_LENGTH

    def test_length_clamped_to_maximum(self) -> None:
        gen = PasswordGenerator(length=9999)
        assert len(gen.generate()) <= MAX_LENGTH

    def test_contains_uppercase(self, gen: PasswordGenerator) -> None:
        for _ in range(10):
            pw = gen.generate()
            assert any(c in string.ascii_uppercase for c in pw), \
                f"No uppercase in: {pw}"

    def test_contains_lowercase(self, gen: PasswordGenerator) -> None:
        for _ in range(10):
            pw = gen.generate()
            assert any(c in string.ascii_lowercase for c in pw), \
                f"No lowercase in: {pw}"

    def test_contains_digit(self, gen: PasswordGenerator) -> None:
        for _ in range(10):
            pw = gen.generate()
            assert any(c in string.digits for c in pw), \
                f"No digit in: {pw}"

    def test_contains_special_character(self, gen: PasswordGenerator) -> None:
        special = PasswordGenerator.SPECIAL
        for _ in range(10):
            pw = gen.generate()
            assert any(c in special for c in pw), \
                f"No special char in: {pw}"

    def test_generates_different_passwords(self, gen: PasswordGenerator) -> None:
        passwords = {gen.generate() for _ in range(50)}
        # With 16-char passwords over a large alphabet the probability of
        # collision is astronomically small
        assert len(passwords) > 45

    def test_characters_from_expected_alphabet(self, gen: PasswordGenerator) -> None:
        alphabet = set(
            PasswordGenerator.UPPERCASE
            + PasswordGenerator.LOWERCASE
            + PasswordGenerator.DIGITS
            + PasswordGenerator.SPECIAL
        )
        for _ in range(10):
            for ch in gen.generate():
                assert ch in alphabet, f"Unexpected character: {ch!r}"


# ---------------------------------------------------------------------------
# validate_strength
# ---------------------------------------------------------------------------

class TestValidateStrength:
    def test_valid_strong_password(self) -> None:
        valid, errors = PasswordGenerator.validate_strength("TestPass1!")
        assert valid is True
        assert errors == []

    def test_too_short(self) -> None:
        valid, errors = PasswordGenerator.validate_strength("Tp1!")
        assert valid is False
        assert any("8" in e for e in errors)

    def test_no_uppercase(self) -> None:
        valid, errors = PasswordGenerator.validate_strength("testpass1!")
        assert valid is False
        assert any("uppercase" in e.lower() for e in errors)

    def test_no_lowercase(self) -> None:
        valid, errors = PasswordGenerator.validate_strength("TESTPASS1!")
        assert valid is False
        assert any("lowercase" in e.lower() for e in errors)

    def test_no_digit(self) -> None:
        valid, errors = PasswordGenerator.validate_strength("TestPass!!")
        assert valid is False
        assert any("digit" in e.lower() for e in errors)

    def test_no_special(self) -> None:
        valid, errors = PasswordGenerator.validate_strength("TestPass11")
        assert valid is False
        assert any("special" in e.lower() for e in errors)

    def test_multiple_failures_reported(self) -> None:
        valid, errors = PasswordGenerator.validate_strength("weak")
        assert valid is False
        assert len(errors) > 1

    def test_generated_password_passes_validation(self, gen: PasswordGenerator) -> None:
        for _ in range(20):
            pw = gen.generate()
            valid, errors = PasswordGenerator.validate_strength(pw)
            assert valid is True, f"Generated password failed validation: {pw!r} — {errors}"
