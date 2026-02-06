import os
import sys
from pathlib import Path
import unittest

import httpx

base_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(base_dir / "app"))
sys.path.insert(0, str(base_dir / "tests"))

from test_helpers import FakeResponse


class TestPipelineIntegration(unittest.IsolatedAsyncioTestCase):
    async def test_full_pipeline(self):
        os.environ["OPENROUTER_API_KEY"] = "test-key"

        import importlib
        import config
        config.settings.OPENROUTER_API_KEY = "test-key"
        import main as main_module
        importlib.reload(main_module)

        async def fake_red_flag_create(*_args, **_kwargs):
            return FakeResponse(
                '{"has_red_flags": false, "flags_detected": [], "severity_score": 0.2, "esi_level": 3, "confidence": 0.7, "reasoning": "No red flags"}'
            )

        async def fake_final_create(*_args, **_kwargs):
            return FakeResponse('{"esi_level": 3, "confidence": 0.8, "reasoning": "Needs resources"}')

        main_module.detector.client.chat.completions.create = fake_red_flag_create
        main_module.final_detector.client.chat.completions.create = fake_final_create

        async with httpx.AsyncClient(app=main_module.app, base_url="http://test") as client:
            response = await client.post(
                "/classify",
                json={
                    "case_text": "41-year-old male with wrist pain and laceration. HR 90, RR 18, BP 120/80.",
                },
            )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("esi_level", data)
        self.assertIn("intermediate", data)
        self.assertEqual(data["esi_level"], 3)
