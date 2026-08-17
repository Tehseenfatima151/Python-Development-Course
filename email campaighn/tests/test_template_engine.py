"""Unit tests for TemplateEngine."""

import tempfile
import unittest
from pathlib import Path

from src.template_engine import TemplateEngine


class TestTemplateEngine(unittest.TestCase):
    """Test suite for HTML and subject personalization."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_placeholder_replacement(self) -> None:
        raw_html = "<h1>Hello {{name}}</h1><p>Special offer: {{offer}} valid until {{date}}.</p>"
        tpl_file = self.temp_path / "template.html"
        tpl_file.write_text(raw_html, encoding="utf-8")

        engine = TemplateEngine(tpl_file)
        context = {
            "name": "Ali",
            "offer": "50% Discount",
            "date": "August 30, 2026",
        }
        result = engine.render_html(context)

        self.assertIn("<h1>Hello Ali</h1>", result)
        self.assertIn("50% Discount", result)
        self.assertIn("August 30, 2026", result)

    def test_subject_personalization(self) -> None:
        engine = TemplateEngine(self.temp_path / "dummy.html")
        subject = "Exclusive Offer for {{name}} - Don't miss out {{name}}!"
        rendered = engine.render_subject(subject, {"name": "Sara"})
        self.assertEqual(rendered, "Exclusive Offer for Sara - Don't miss out Sara!")

    def test_missing_placeholder_preserved_or_safe(self) -> None:
        engine = TemplateEngine(self.temp_path / "dummy.html")
        subject = "Hello {{name}}, welcome to {{unknown_key}}!"
        rendered = engine.render_subject(subject, {"name": "Ahmed"})
        self.assertEqual(rendered, "Hello Ahmed, welcome to {{unknown_key}}!")

    def test_whitespace_in_placeholders(self) -> None:
        engine = TemplateEngine(self.temp_path / "dummy.html")
        template = "Hello {{  name   }} from {{ company }}!"
        rendered = engine.render_string(template, {"name": "Fatima", "company": "Apex Inc"})
        self.assertEqual(rendered, "Hello Fatima from Apex Inc!")

    def test_missing_template_file(self) -> None:
        engine = TemplateEngine(self.temp_path / "does_not_exist.html")
        with self.assertRaises(FileNotFoundError):
            engine.render_html({"name": "Test"})


if __name__ == "__main__":
    unittest.main()
