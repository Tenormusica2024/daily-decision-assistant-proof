from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from decision_engine import build_decision_brief, load_json, render_markdown, score_signal, stable_queue_id


def test_sample_brief_groups_focus_defer_and_no_go():
    signals = load_json(ROOT / "samples" / "daily_signals.json")
    rules = load_json(ROOT / "samples" / "decision_rules.json")
    brief = build_decision_brief(signals, rules)

    assert brief["summary"]["signals_scanned"] == 5
    assert brief["summary"]["focus_count"] == 2
    assert brief["summary"]["defer_count"] == 2
    assert brief["summary"]["no_go_count"] == 1
    assert brief["today_focus"][0]["title"] == "Stakeholder workflow review at 15:00"
    assert brief["no_go"][0]["recommended_next_step"] == "do_not_execute_until_unblocked"


def test_external_focus_item_goes_to_confirmation_queue():
    signals = load_json(ROOT / "samples" / "daily_signals.json")
    rules = load_json(ROOT / "samples" / "decision_rules.json")
    brief = build_decision_brief(signals, rules)

    assert brief["summary"]["confirmation_queue_count"] == 1
    item = brief["confirmation_queue"][0]
    assert item["signal_id"] == "sig-001"
    assert item["recommended_action"] == "prepare_confirmation_before_external_action"


def test_confirmation_queue_id_is_stable():
    first = stable_queue_id("calendar", "sig-001", "Stakeholder workflow review at 15:00")
    second = stable_queue_id("calendar", "sig-001", "Stakeholder workflow review at 15:00")

    assert first == second
    assert len(first) == 12


def test_markdown_contains_safety_sections():
    signals = load_json(ROOT / "samples" / "daily_signals.json")
    rules = load_json(ROOT / "samples" / "decision_rules.json")
    markdown = render_markdown(build_decision_brief(signals, rules))

    assert "Today Focus" in markdown
    assert "No-Go / Blocked" in markdown
    assert "Confirmation Queue" in markdown
    assert "no-send" in markdown


def test_string_boolean_fields_are_not_treated_as_truthy_by_default():
    rules = load_json(ROOT / "samples" / "decision_rules.json")
    item = score_signal({
        "id": "sig-string-bool",
        "source": "sample",
        "title": "String boolean guard",
        "urgency": 3,
        "value": 3,
        "effort": 1,
        "deadline_hours": 48,
        "blocked": "false",
        "requires_external_action": "false",
    }, rules)

    assert item["blocked"] is False
    assert item["requires_external_action"] is False
    assert item["recommended_next_step"] == "work_locally_first"

