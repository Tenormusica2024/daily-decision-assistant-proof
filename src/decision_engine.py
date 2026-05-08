from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def stable_queue_id(source: str, signal_id: str | None, title: str) -> str:
    raw = f"{source}|{signal_id or ''}|{title}".lower().encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:12]


def _number(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


def score_signal(signal: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
    weights = rules.get("score_weights") or {}
    urgency = _number(signal.get("urgency"))
    value = _number(signal.get("value"))
    effort = _number(signal.get("effort"))
    deadline_hours = _number(signal.get("deadline_hours"), default=9999)
    blocked = _bool(signal.get("blocked"))

    score = (
        urgency * _number(weights.get("urgency"), 1)
        + value * _number(weights.get("value"), 1)
        + effort * _number(weights.get("effort"), 0)
    )
    reasons: list[str] = [
        f"urgency={urgency}",
        f"value={value}",
        f"effort={effort}",
    ]

    if deadline_hours <= _number(rules.get("deadline_boost_hours"), 24):
        boost = _number(weights.get("deadline_boost"), 0)
        score += boost
        reasons.append(f"deadline_boost=+{boost}")

    if blocked:
        penalty = _number(weights.get("blocked_penalty"), -20)
        score += penalty
        reasons.append(f"blocked_penalty={penalty}")

    return {
        "id": signal.get("id"),
        "source": signal.get("source"),
        "title": signal.get("title"),
        "kind": signal.get("kind"),
        "score": score,
        "blocked": blocked,
        "requires_external_action": _bool(signal.get("requires_external_action")),
        "reason": ", ".join(reasons),
        "recommended_next_step": recommend_next_step(signal, score, rules),
        "note": signal.get("note"),
        "blocker_reason": signal.get("blocker_reason"),
    }


def recommend_next_step(signal: dict[str, Any], score: int, rules: dict[str, Any]) -> str:
    if _bool(signal.get("blocked")):
        return "do_not_execute_until_unblocked"
    if _bool(signal.get("requires_external_action")):
        return "prepare_confirmation_before_external_action"
    if score <= _number(rules.get("low_value_threshold"), 6):
        return "defer_or_skip"
    return "work_locally_first"


def build_confirmation_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": stable_queue_id(
            str(item.get("source") or "sample"),
            str(item.get("id") or ""),
            str(item.get("title") or ""),
        ),
        "source": item.get("source"),
        "signal_id": item.get("id"),
        "title": item.get("title"),
        "recommended_action": item.get("recommended_next_step"),
        "reason": item.get("reason"),
    }


def build_decision_brief(signals: list[dict[str, Any]], rules: dict[str, Any]) -> dict[str, Any]:
    scored = [score_signal(signal, rules) for signal in signals]
    scored.sort(key=lambda item: (-_number(item.get("score")), str(item.get("title") or "")))

    no_go = [item for item in scored if item.get("blocked")]
    candidates = [item for item in scored if not item.get("blocked")]
    focus = candidates[: _number(rules.get("focus_limit"), 2)]
    focus_ids = {item.get("id") for item in focus}
    defer = [item for item in candidates if item.get("id") not in focus_ids][:_number(rules.get("defer_limit"), 3)]
    confirmation_queue = [build_confirmation_item(item) for item in focus if item.get("requires_external_action")]

    return {
        "summary": {
            "signals_scanned": len(signals),
            "focus_count": len(focus),
            "defer_count": len(defer),
            "no_go_count": len(no_go),
            "confirmation_queue_count": len(confirmation_queue),
            "safety": rules.get("safety", "sample-first / no-send / no-modify"),
        },
        "today_focus": focus,
        "defer": defer,
        "no_go": no_go,
        "confirmation_queue": confirmation_queue,
    }


def render_markdown(brief: dict[str, Any]) -> str:
    lines = [
        "# Daily Decision Assistant Proof Report",
        "",
        f"- scanned: `{brief['summary']['signals_scanned']}`",
        f"- safety: `{brief['summary']['safety']}`",
        f"- today focus: `{brief['summary']['focus_count']}`",
        f"- defer: `{brief['summary']['defer_count']}`",
        f"- no-go: `{brief['summary']['no_go_count']}`",
        f"- confirmation queue: `{brief['summary']['confirmation_queue_count']}`",
        "",
        "## Today Focus",
        "",
    ]
    for item in brief["today_focus"]:
        lines.extend([
            f"### {item['title']}",
            f"- score: `{item['score']}`",
            f"- source: `{item['source']}` / kind: `{item['kind']}`",
            f"- reason: {item['reason']}",
            f"- next_step: `{item['recommended_next_step']}`",
            "",
        ])

    lines.extend(["## Defer", ""])
    for item in brief["defer"]:
        lines.append(f"- {item['title']} — score `{item['score']}` / `{item['recommended_next_step']}`")
    if not brief["defer"]:
        lines.append("- none")

    lines.extend(["", "## No-Go / Blocked", ""])
    for item in brief["no_go"]:
        blocker = item.get("blocker_reason") or "blocked"
        lines.append(f"- {item['title']} — {blocker}")
    if not brief["no_go"]:
        lines.append("- none")

    lines.extend(["", "## Confirmation Queue", ""])
    for item in brief["confirmation_queue"]:
        lines.append(f"- `{item['id']}` {item['title']} -> `{item['recommended_action']}`")
    if not brief["confirmation_queue"]:
        lines.append("- none")

    return "\n".join(lines).rstrip() + "\n"
