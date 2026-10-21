"""
Unit Tests for Resume Parser Module
"""

import unittest
import io
from modules.resume_parser import validate_resume_file, sanitize_text, extract_text_from_pdf, parse_resume


class TestResumeParser(unittest.TestCase):

    def test_validate_resume_valid_extension(self):
        class MockFile:
            name = "candidate_resume.pdf"
            size = 1024 * 50  # 50 KB

        val = validate_resume_file(MockFile())
        self.assertTrue(val["valid"])
        self.assertEqual(val["extension"], ".pdf")

    def test_validate_resume_invalid_extension(self):
        class MockFile:
            name = "malicious_script.exe"
            size = 1024

        val = validate_resume_file(MockFile())
        self.assertFalse(val["valid"])
        self.assertIn("Unsupported file format", val["error"])

    def test_validate_resume_oversized(self):
        class MockFile:
            name = "huge_file.pdf"
            size = 15 * 1024 * 1024  # 15 MB

        val = validate_resume_file(MockFile())
        self.assertFalse(val["valid"])
        self.assertIn("exceeds maximum allowed size", val["error"])

    def test_sanitize_text(self):
        raw = "Hello\x00\x05World!   This  is   a test.\n\n\n\nNew paragraph."
        clean = sanitize_text(raw)
        self.assertNotIn("\x00", clean)
        self.assertNotIn("\x05", clean)
        self.assertIn("Hello World!", clean)
        self.assertNotIn("\n\n\n\n", clean)

    def test_empty_file_handling(self):
        res = parse_resume(None)
        self.assertFalse(res["success"])
        self.assertIn("No file was provided", res["error"])


if __name__ == "__main__":
    unittest.main()
