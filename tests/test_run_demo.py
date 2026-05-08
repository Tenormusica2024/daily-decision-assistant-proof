from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_run_demo_generates_reports():
    result = subprocess.run(
        [sys.executable, "-X", "utf8", "run_demo.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "no-send" in result.stdout
    assert (ROOT / "outputs" / "daily_decision_brief.md").exists()
    assert (ROOT / "outputs" / "daily_decision_brief.json").exists()
