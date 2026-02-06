import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from detectors.vital_signal import VitalSignalDetector


class TestVitalSignalLayer(unittest.IsolatedAsyncioTestCase):
    async def test_vital_assessment_with_extraction(self):
        detector = VitalSignalDetector()
        extracted = {
            "age": 30,
            "vitals": {"hr": 120, "rr": 28, "sbp": 110, "dbp": 70, "temp_f": 99.0, "spo2": 95},
        }
        result = await detector.assess("", extracted)

        self.assertEqual(result["age"], 30)
        self.assertIn("hr", result["vitals"])
        self.assertIn("abnormalities", result)
        self.assertFalse(result["critical"])