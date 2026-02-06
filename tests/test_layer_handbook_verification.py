import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from detectors.handbook_verification import HandbookVerificationDetector


class TestHandbookVerificationLayer(unittest.IsolatedAsyncioTestCase):
    async def test_handbook_verification(self):
        detector = HandbookVerificationDetector()
        result = await detector.verify(3, "test case")

        self.assertEqual(result["esi_level"], 3)
        self.assertIn("confidence", result)
        self.assertIn("rag", result)