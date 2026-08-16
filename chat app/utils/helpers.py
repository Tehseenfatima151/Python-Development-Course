import re
import hashlib
from datetime import datetime, timezone
from typing import Tuple

# Curated palette of 16 vibrant, distinct, accessible colors with high contrast on dark & light surfaces
AVATAR_PALETTE = [
    "#3b82f6",  # Blue
    "#10b981",  # Emerald
    "#8b5cf6",  # Violet
    "#f59e0b",  # Amber
    "#ec4899",  # Pink
    "#06b6d4",  # Cyan
    "#14b8a6",  # Teal
    "#f97316",  # Orange
    "#6366f1",  # Indigo
    "#84cc16",  # Lime
    "#d946ef",  # Fuchsia
    "#0ea5e9",  # Sky
    "#e11d48",  # Rose
    "#10b981",  # Mint
    "#a855f7",  # Purple
    "#eab308",  # Yellow Gold
]

ALLOWED_REACTIONS = {"👍", "❤️", "😂", "🔥", "👏"}


def get_username_color(username: str) -> str:
    """
    Deterministically computes a color hex from username hash.
    Ensures the same user always receives the exact same distinguishable color.
    """
    if not username:
        return AVATAR_PALETTE[0]
    cleaned = username.strip().lower()
    # MD5 hash modulo palette length
    hash_val = int(hashlib.md5(cleaned.encode("utf-8")).hexdigest(), 16)
    return AVATAR_PALETTE[hash_val % len(AVATAR_PALETTE)]


def sanitize_text(text: str) -> str:
    """
    Sanitize text by removing dangerous unprintable control characters,
    normalizing whitespace, while preserving emojis and international characters.
    """
    if not text:
        return ""
    # Strip null bytes and control chars (except standard whitespace: tab, newline, cr)
    cleaned = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)
    # Strip leading and trailing whitespace
    return cleaned.strip()


def validate_username(username: str, max_length: int = 30) -> Tuple[bool, str]:
    """
    Validate username requirements:
    - Must not be empty
    - Must not exceed max_length
    - Must be between 2 and max_length characters
    - Must contain valid characters (letters, numbers, spaces, underscores, dashes, dots)
    """
    if not username or not isinstance(username, str):
        return False, "Username is required."
    
    cleaned = sanitize_text(username)
    if len(cleaned) < 2:
        return False, "Username must be at least 2 characters long."
    if len(cleaned) > max_length:
        return False, f"Username cannot exceed {max_length} characters."
    
    # Check for valid characters
    if not re.match(r"^[\w\s.\-]+$", cleaned, re.UNICODE):
        return False, "Username contains invalid special characters."
    
    return True, ""


def validate_room(room: str, max_length: int = 50) -> Tuple[bool, str]:
    """
    Validate room name:
    - Must not be empty
    - Must not exceed max_length
    - Between 2 and max_length characters
    """
    if not room or not isinstance(room, str):
        return False, "Room name is required."
    
    cleaned = sanitize_text(room)
    if len(cleaned) < 2:
        return False, "Room name must be at least 2 characters long."
    if len(cleaned) > max_length:
        return False, f"Room name cannot exceed {max_length} characters."
    
    if not re.match(r"^[\w\s.\-#]+$", cleaned, re.UNICODE):
        return False, "Room name contains invalid characters."
    
    return True, ""


def validate_room_description(desc: str, max_length: int = 255) -> Tuple[bool, str]:
    """Validate room description length and characters."""
    if desc is None:
        return True, ""
    cleaned = sanitize_text(desc)
    if len(cleaned) > max_length:
        return False, f"Room description cannot exceed {max_length} characters."
    return True, ""


def validate_message(content: str, max_length: int = 1000) -> Tuple[bool, str]:
    """
    Validate message content:
    - Must not be empty
    - Must not exceed max_length
    """
    if not content or not isinstance(content, str):
        return False, "Message content cannot be empty."
    
    cleaned = sanitize_text(content)
    if len(cleaned) == 0:
        return False, "Message cannot be empty or just whitespace."
    if len(cleaned) > max_length:
        return False, f"Message exceeds maximum length of {max_length} characters."
    
    return True, ""


def validate_reaction(reaction: str) -> Tuple[bool, str]:
    """Validate emoji reaction against allowed set."""
    if not reaction or not isinstance(reaction, str):
        return False, "Reaction cannot be empty."
    cleaned = sanitize_text(reaction)
    if cleaned not in ALLOWED_REACTIONS:
        return False, f"Invalid reaction '{cleaned}'. Allowed reactions: {', '.join(ALLOWED_REACTIONS)}"
    return True, ""


def get_utc_now_iso() -> str:
    """Return current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()
