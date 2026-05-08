# Public Export Checklist

Use this checklist before publishing or reusing this proof.

## Required checks

- The demo runs with only `samples/daily_signals.json` and `samples/decision_rules.json`.
- No real calendar, email, chat, or client data is included.
- No private issue or support-ticket content is included.
- No private knowledge-base output is included.
- No token, credential, or local absolute path is required.
- Default behavior is no-send / no-modify / no-execute.
- Action-worthy items go to a confirmation queue instead of being executed.
- Focus, defer, and no-go groups are explainable from sample inputs.

## Pre-export commands

```powershell
python -m pytest tests -q
python -X utf8 run_demo.py
python scripts/check_public_boundary.py
```

## Public repository description draft

```text
Sample-first AI secretary proof for turning daily signals into a focus/defer/no-go decision brief.
```
