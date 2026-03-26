# Collaborator Stage 1 — Task Folder And Handoff State

## Scaffold The Task Folder

Create:

- `DATA_INTAKE.md`
- `TASK_INTAKE.md`
- `scripts/DATA_PIPELINE.md`
- `PITFALLS.md`
- `CONTEXT.md` copied from `docs/task_impl_guides/templates/CONTEXT_EXTERNAL.md`

As soon as the task folder exists, the task has officially started.

---

## Runtime Directory Structure

```text
<runtime_root>/<domain_name>/<task_name>/<variant_name>/
  input/           <- agent-visible runtime input only
  output/          <- agent writes here
  reference/       <- evaluator-only ground truth
  output_test_pos/ <- evaluator fixture
  output_test_neg/ <- evaluator fixture
  software/        <- app shortcuts or runtime assets
```

Record these paths in `CONTEXT.md` under `## Important Paths`.

Keep the boundary explicit:

- `tasks/<domain_name>/<task_name>/` stores docs, code, scripts, and review artifacts
- the runtime directories store data or runtime assets only
- do not place planning docs or review outputs into runtime `input/`, `output/`, or `reference/`

---

## Handoff State Rules

Collaborator tasks do not write internal DB status.

Instead:

- keep the active checklist pasted in `CONTEXT.md`
- update `Current stage` and `Current handoff status` in `CONTEXT.md`
- append a short entry to the handoff log when Stage 1 becomes stable

Use consistent handoff-state phrases such as:

- `stage1_in_progress`
- `stage1_planning_stable`
- `stage2_in_progress`
- `stage2_tested_ready_for_admin_handoff`
