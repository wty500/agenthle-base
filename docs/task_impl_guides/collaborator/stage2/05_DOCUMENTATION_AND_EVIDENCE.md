# Collaborator Stage 2 — Documentation And Evidence

## Evidence Screenshots (`important_observations/`)

When working on the runtime machine during implementation, testing, or debugging, take a screenshot whenever visual evidence helps explain what happened. Save it to `important_observations/` in the task folder.

When to screenshot:

- software UI state after setup or a key step completes
- test output showing pass or fail
- unexpected error dialogs or wrong visual results
- before or after comparisons when fixing issues

Naming convention: `<phase>_<short_description>.png`.

This directory is gitignored via `tasks/**/important_observations/`. The screenshots stay local as a reference for the admin handoff.

---

## Required Living Documents

Keep these documents up to date:

- `DATA_INTAKE.md`
- `TASK_INTAKE.md`
- `CONTEXT.md`
- `PITFALLS.md`
- `scripts/DATA_PIPELINE.md`
- `README.md`
- `REPRO_COMMANDS.md`

If Stage 2 cannot complete software setup without user interaction, record the handoff item clearly in:

- `CONTEXT.md`
- `PITFALLS.md`
- `README.md` if the operator needs the instruction during reruns

---

## Do Not Commit

Do not commit:

- `.env`
- `tasks/<domain>/<task>/tmp/`

Each task folder may keep a local `tmp/` directory for ephemeral data such as transient IP notes, temporary analysis artifacts, or raw review output before summarization.
