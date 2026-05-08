# Daily Decision Assistant Proof

A public-safe proof slice for an AI secretary that turns mixed daily signals into a small decision brief without requiring Gmail, Calendar, LLMWIKI, or external APIs.

## One-minute summary

This repository demonstrates a practical AI-secretary pattern:

```text
sample daily signals -> scoring -> today focus / defer / no-go -> confirmation queue
```

It is meant as a portfolio proof for:

- daily prioritization support
- human-in-the-loop decision boundaries
- safe action queues before external side effects
- deterministic Python implementation with synthetic fixtures and tests

## For reviewers

Review these first:

1. `outputs/daily_decision_brief.md` — generated decision brief
2. `src/decision_engine.py` — deterministic scoring and routing logic
3. `tests/` — behavior and safety checks
4. `docs/privacy-boundary.md` — what must not be published
5. `docs/portfolio-copy.md` — how to describe this proof in portfolio/proposal contexts

## What this proves

This proof shows that an AI secretary does not need to immediately execute tasks. It can first:

- collect mixed signals into one small daily view
- rank what should be handled today
- separate low-value or blocked items into defer/no-go groups
- place external actions into a confirmation queue
- keep the default demo sample-first, deterministic, and public-safe

## Scope boundaries

This is not:

- a production task manager
- a calendar/email integration
- an autonomous executor
- a hosted SaaS demo

It is a focused proof of the daily decision and confirmation pattern.

## Quick demo

From this proof directory:

```powershell
python -X utf8 run_demo.py
```

Run tests:

```powershell
python -m pytest tests -q
```

## Safety model

The default mode is:

- no external APIs
- no email sending
- no calendar mutation
- no task system mutation
- no automatic action execution

Action-worthy recommendations are represented as confirmation queue entries for human review.

## Public/private boundary

This repository uses synthetic fixtures only. It should not contain real calendar events, real emails, client details, private GitHub Issue content, local absolute paths, tokens, or LLMWIKI/curiosity-wiki outputs.

See:

- `docs/privacy-boundary.md`
- `docs/public-export-checklist.md`
- `docs/portfolio-copy.md`
