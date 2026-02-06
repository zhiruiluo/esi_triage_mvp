import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from detectors.extraction import ExtractionDetector


class TestExtractionLayer(unittest.TestCase):
    def test_extract_basic_fields(self):
        detector = ExtractionDetector()
        text = "32-year-old female with chest pain. Vital signs: HR 110, RR 22, BP 140/90, T 99.1F, SpO2 94%"
        result = detector.extract(text)

        self.assertEqual(result["age"], 32)
        self.assertEqual(result["chief_complaint"], "Chest Pain")
        self.assertEqual(result["vitals"]["hr"], 110)
        self.assertEqual(result["vitals"]["rr"], 22)
        self.assertEqual(result["vitals"]["sbp"], 140)
        self.assertEqual(result["vitals"]["dbp"], 90)
        self.assertEqual(result["vitals"]["temp_f"], 99.1)
        self.assertEqual(result["vitals"]["spo2"], 94)
        self.assertIn("chest pain", result["keywords"])