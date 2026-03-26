# Collaborator Stage 1 — Data Source And Environment

## Source Of Truth

For collaborator tasks, the source of truth is the real data package you were given plus the repo task folder you are building.

Typical source patterns:

- a shared folder or drive
- a zip or tar archive
- a local working copy from the submitter
- a manually transferred set of files from email, chat, or cloud storage

Document the exact source path or delivery mechanism in `DATA_INTAKE.md`.

---

## What Collaborators Should Not Assume

Do **not** assume access to:

- internal Postgres tables such as `users`, `submissions`, or `task_implementations`
- helper scripts that write admin status
- raw submission lookups through backend models
- `gs://agenthle_formdata/...`
- `gs://agenthle/...`

If some metadata is missing, record that gap in `DATA_INTAKE.md` and `CONTEXT.md` rather than inventing a database-backed source of truth.

---

## Questions To Resolve Early

Answer these from the files you actually have:

| Question | Why it matters |
|---|---|
| What is the true raw source? | Avoid planning against stale or partial copies |
| Which files are usable vs noise? | Prevents task designs built on irrelevant assets |
| What constitutes one variant? | Drives `load()` and evaluation layout |
| What metadata is missing? | Exposes planning risks early |
| Can the available data support the intended verification method? | The task definition must match the data |

---

## `DATA_INTAKE.md` Expectations

Capture:

- exact source location and how it was received
- raw file inventory
- formats and approximate sizes
- variant boundaries
- candidate runtime inputs, references, and noise
- likely sources for realistic `output_test_pos/` and `output_test_neg/`
- missing metadata, software assumptions, and unresolved questions

If you only have a working copy rather than the original delivery artifact, say so explicitly.
