"""Smoke test for the Streamlit UI (skipped without dashboard extras)."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


STREAMLIT_AVAILABLE = importlib.util.find_spec("streamlit") is not None


@unittest.skipUnless(STREAMLIT_AVAILABLE, "install the dashboard optional dependencies")
class StreamlitDashboardTests(unittest.TestCase):
    def test_default_dashboard_run_has_no_ui_exception(self) -> None:
        from streamlit.testing.v1 import AppTest

        app_path = Path(__file__).resolve().parents[1] / "dashboard" / "app.py"
        dashboard = AppTest.from_file(str(app_path), default_timeout=40).run()
        self.assertEqual(len(dashboard.exception), 0)
        self.assertEqual(dashboard.button[0].label, "Chạy thuật toán")

        dashboard.button[0].click().run(timeout=40)
        self.assertEqual(len(dashboard.exception), 0)
        self.assertEqual(len(dashboard.error), 0)
        metric_values = {metric.label: metric.value for metric in dashboard.metric}
        self.assertEqual(metric_values["Trạng thái"], "Hội tụ")
        self.assertIn("Residual Eq. (19)", metric_values)


if __name__ == "__main__":
    unittest.main()

