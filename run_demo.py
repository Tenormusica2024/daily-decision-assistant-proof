from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from decision_engine import build_decision_brief, load_json, render_markdown  # noqa: E402


def main() -> int:
    signals = ROOT / "samples" / "daily_signals.json"
    rules = ROOT / "samples" / "decision_rules.json"
    output_dir = ROOT / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    brief = build_decision_brief(load_json(signals), load_json(rules))
    report_md = output_dir / "daily_decision_brief.md"
    report_json = output_dir / "daily_decision_brief.json"

    report_md.write_text(render_markdown(brief), encoding="utf-8", newline="\n")
    report_json.write_text(json.dumps(brief, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(f"wrote {report_md.relative_to(ROOT)}")
    print(f"wrote {report_json.relative_to(ROOT)}")
    print("safety: sample-first / no-send / no-modify / confirmation-required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
