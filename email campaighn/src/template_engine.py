"""Template rendering engine for HTML body and subject line personalization.

Loads HTML email templates and performs dynamic placeholder replacement
(e.g., {{name}}, {{email}}, {{company}}, {{offer}}, {{date}}) across email
bodies and subject headers.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping


# Regex pattern to match {{ placeholder }} or {{placeholder}}
PLACEHOLDER_REGEX = re.compile(r"\{\{\s*([a-zA-Z0-9_-]+)\s*\}\}")


class TemplateEngine:
    """Handles HTML template loading and placeholder substitution."""

    def __init__(self, template_path: Path | str) -> None:
        self.template_path = Path(template_path)
        self._cached_template: str | None = None

    def load_template(self, force_reload: bool = False) -> str:
        """Load HTML template content from file.

        Raises:
            FileNotFoundError: If the template file does not exist.
            ValueError: If the template file is empty.
        """
        if self._cached_template is not None and not force_reload:
            return self._cached_template

        if not self.template_path.exists():
            raise FileNotFoundError(f"Email template not found at: {self.template_path}")

        try:
            content = self.template_path.read_text(encoding="utf-8")
        except Exception as e:
            raise ValueError(f"Failed to read email template ({self.template_path}): {e}")

        if not content.strip():
            raise ValueError(f"Email template is empty: {self.template_path}")

        self._cached_template = content
        return content

    @staticmethod
    def render_string(template_str: str, context: Mapping[str, Any]) -> str:
        """Replace all {{ key }} placeholders in template_str using context mapping.

        If a placeholder key is missing from context, it retains the placeholder or
        replaces it gracefully if an empty fallback is preferred.
        """
        if not template_str:
            return ""

        # Normalize context keys to lowercase for flexible matching
        normalized_context = {str(k).lower(): str(v) for k, v in context.items()}

        def replace_match(match: re.Match) -> str:
            key = match.group(1).lower()
            return normalized_context.get(key, match.group(0))

        return PLACEHOLDER_REGEX.sub(replace_match, template_str)

    def render_html(self, context: Mapping[str, Any]) -> str:
        """Render the loaded HTML template with the given context dictionary."""
        raw_html = self.load_template()
        return self.render_string(raw_html, context)

    def render_subject(self, subject_template: str, context: Mapping[str, Any]) -> str:
        """Render a personalized subject line using context dictionary."""
        return self.render_string(subject_template, context)
