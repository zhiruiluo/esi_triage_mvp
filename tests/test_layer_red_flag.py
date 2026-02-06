import os
import sys
from pathlib import Path
import unittest
from unittest.mock import patch

os.environ["OPENROUTER_API_KEY"] = "test-key"

base_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(base_dir / "app"))
sys.path.insert(0, str(base_dir / "tests"))

from config import settings
from detectors.red_flag import RedFlagDetector
from test_helpers import FakeResponse


class TestRedFlagLayer(unittest.IsolatedAsyncioTestCase):
    async def test_red_flag_with_mocked_llm(self):
        os.environ["OPENROUTER_API_KEY"] = "test-key"
        settings.OPENROUTER_API_KEY = "test-key"

        fake_content = (
            '{"has_red_flags": true, "flags_detected": ["Chest pain"], '
            '"severity_score": 0.8, "esi_level": 2, "confidence": 0.9, "reasoning": "High risk"}'
        )

        async def fake_create(*_args, **_kwargs):
            return FakeResponse(fake_content)

        with patch("detectors.red_flag.AsyncOpenAI") as mock_client:
            instance = mock_client.return_value
            instance.chat.completions.create = fake_create

            detector = RedFlagDetector()
            result = await detector.classify("55yo with chest pain")

        self.assertTrue(result["has_red_flags"])
        self.assertEqual(result["esi"], 2)
        self.assertEqual(result["flags"], ["Chest pain"])
        self.assertGreater(result["confidence"], 0.5)