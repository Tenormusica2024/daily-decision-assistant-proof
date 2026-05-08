# Privacy Boundary

This proof slice is sample-first and public-safe by default.

## Safe to publish

- Synthetic daily signal fixtures under `samples/`
- Generic scoring rules
- Deterministic prioritization logic
- Confirmation queue examples
- Markdown/JSON reports generated from synthetic data

## Do not publish

- Real calendar entries
- Real email or chat messages
- Real customer names, private project names, or NDA details
- Private issue or support-ticket content
- Private knowledge-base outputs
- API tokens, OAuth credentials, local scheduler state
- Local absolute paths that reveal private environment details

## Default safety model

The default demo is:

- no external API
- no calendar mutation
- no email send
- no task update
- no automatic execution

The assistant recommends a decision; a human approves any external action.
