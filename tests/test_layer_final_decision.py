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
from detectors.final_decision import FinalDecisionDetector
from test_helpers import FakeResponse


class TestFinalDecisionLayer(unittest.IsolatedAsyncioTestCase):
    async def test_final_decision_with_mocked_llm(self):
        os.environ["OPENROUTER_API_KEY"] = "test-key"
        settings.OPENROUTER_API_KEY = "test-key"

        fake_content = '{"esi_level": 3, "confidence": 0.8, "reasoning": "Resources needed"}'

        async def fake_create(*_args, **_kwargs):
            return FakeResponse(fake_content)

        with patch("detectors.final_decision.AsyncOpenAI") as mock_client:
            instance = mock_client.return_value
            instance.chat.completions.create = fake_create

            detector = FinalDecisionDetector()
            result = await detector.decide("case", {"esi_level": 3})

        self.assertEqual(result["esi"], 3)
        self.assertGreater(result["confidence"], 0.5)
        self.assertTrue(result["reason"].startswith("Resources"))