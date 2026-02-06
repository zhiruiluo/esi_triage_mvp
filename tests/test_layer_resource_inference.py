import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from detectors.resource_inference import ResourceInferenceDetector


class TestResourceInferenceLayer(unittest.IsolatedAsyncioTestCase):
    async def test_resource_inference_keywords(self):
        detector = ResourceInferenceDetector()
        extracted = {
            "keywords": ["chest pain", "laceration", "wrist"],
        }
        result = await detector.infer("", extracted)

        self.assertGreaterEqual(result["resource_count"], 2)
        self.assertIn("ECG", result["resources"])
        self.assertIn("Sutures", result["resources"])
        self.assertIn("X-ray", result["resources"])