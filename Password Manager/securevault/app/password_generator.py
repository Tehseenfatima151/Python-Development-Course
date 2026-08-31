"""
PasswordGenerator — generates cryptographically secure random passwords.
"""

import secrets
import string

# Default generation settings
DEFAULT_LENGTH = 16
MIN_LENGTH = 8
MAX_LENGTH = 128


class PasswordGenerator:
    """
    Generates strong random passwords using the `secrets` module,
    which is suitable for cryptographic use.

    Every generated password is guaranteed to contain at least one
    character from each required category:
      - Uppercase letters
      - Lowercase letters
      - Digits
      - Special characters
    """

    UPPERCASE = string.ascii_uppercase
    LOWERCASE = string.ascii_lowercase
    DIGITS = string.digits
    SPECIAL = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def __init__(self, length: int = DEFAULT_LENGTH) -> None:
        """
        Initialise the generator with a desired password length.

        Args:
            length: Total length of generated passwords. Must be between
                    MIN_LENGTH and MAX_LENGTH.
        """
        self._length = self._validated_length(length)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def generate(self) -> str:
        """
        Generate and return a secure random password.

        The password is guaranteed to contain at least one character from
        each of the four required categories.

        Returns:
            A secure random password string.
        """
        alphabet = self.UPPERCASE + self.LOWERCASE + self.DIGITS + self.SPECIAL

        # Ensure at least one character from every required category
        mandatory = [
            secrets.choice(self.UPPERCASE),
            secrets.choice(self.LOWERCASE),
            secrets.choice(self.DIGITS),
            secrets.choice(self.SPECIAL),
        ]

        # Fill remaining positions from the full alphabet
        remainder = [secrets.choice(alphabet) for _ in range(self._length - len(mandatory))]

        combined = mandatory + remainder

        # Shuffle with a cryptographically secure shuffle
        for i in range(len(combined) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            combined[i], combined[j] = combined[j], combined[i]

        return "".join(combined)

    @staticmethod
    def validate_strength(password: str) -> tuple[bool, list[str]]:
        """
        Check whether a password meets the minimum strength requirements.

        Requirements:
          - At least 8 characters
          - At least one uppercase letter
          - At least one lowercase letter
          - At least one digit
          - At least one special character

        Args:
            password: The password string to evaluate.

        Returns:
            A tuple of (is_valid: bool, errors: list[str]) where errors
            contains human-readable descriptions of each unmet requirement.
        """
        errors: list[str] = []

        if len(password) < MIN_LENGTH:
            errors.append(f"Password must be at least {MIN_LENGTH} characters long.")
        if not any(c in PasswordGenerator.UPPERCASE for c in password):
            errors.append("Password must contain at least one uppercase letter.")
        if not any(c in PasswordGenerator.LOWERCASE for c in password):
            errors.append("Password must contain at least one lowercase letter.")
        if not any(c in PasswordGenerator.DIGITS for c in password):
            errors.append("Password must contain at least one digit.")
        if not any(c in PasswordGenerator.SPECIAL for c in password):
            errors.append("Password must contain at least one special character.")

        return (len(errors) == 0, errors)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _validated_length(length: int) -> int:
        """Clamp and validate the requested password length."""
        if length < MIN_LENGTH:
            return MIN_LENGTH
        if length > MAX_LENGTH:
            return MAX_LENGTH
        return length
