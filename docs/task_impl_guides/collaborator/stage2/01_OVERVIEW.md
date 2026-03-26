# Collaborator Stage 2 — Overview

Use Stage 2 to turn the Stage 1 plan into a runnable task on the collaborator runtime environment.

## Required Flow

Stage 2 should proceed in this order:

1. Re-confirm the collaborator machine and staged task-ready data.
2. Implement `main.py`, helper scripts, and `run_<taskname>.sh`.
3. Write `README.md` and `REPRO_COMMANDS.md`.
4. Run setup-only testing for `start()`.
5. Run positive evaluation testing against `output_test_pos/`.
6. Run negative evaluation testing against `output_test_neg/`.
7. Record final handoff notes, access grants, and migration blockers in `CONTEXT.md`.

## Stage Boundary Assumption

By the time Stage 2 starts, Stage 1 has already produced task-ready benchmark data in the collaborator runtime layout.

That means:

- task-ready data already exists on the collaborator machine under the planned `domain/task/variant` path
- `main.py` must not perform database or GCS sync work
- `start()` must not hide raw-data staging steps that belong in Stage 1
- `evaluate()` must not fetch reference data from GCS at runtime
