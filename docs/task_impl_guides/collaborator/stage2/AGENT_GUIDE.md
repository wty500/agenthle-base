# Collaborator Stage 2 — Implementation And Testing

> Read this once Stage 1 is stable and the task is ready to become runnable code.

Use `CHECKLIST.md` in this folder as the Stage 2 checklist source. Paste it into `CONTEXT.md` under `## Check List` and keep it current there.

---

## Python Environment

For Stage 2 local Python commands, use `uv run`.

Canonical pattern:

```bash
uv run python ...
```

Use this for:

- local task-side commands
- `cua_bench` setup and evaluation runs
- helper scripts that belong to the task repo

---

## Goal

Implement the task, verify setup and evaluation on the collaborator VM or workstation, and produce a clean admin handoff package.

---

## Read In This Order

1. `01_OVERVIEW.md`
2. `02_COLLABORATOR_VM_AND_RUNTIME_LAYOUT.md`
3. `03_MAIN_PY_AND_EVALUATION.md`
4. `04_TESTING_AND_HANDOFF.md`
5. `05_DOCUMENTATION_AND_EVIDENCE.md`
6. `06_CONTEXT_AND_EXIT.md`

Use this set as the Stage 2 reading stack rather than as a single long reference file.

---

## Exit Criteria

Stage 2 is complete only when:

- the implementation matches `TASK_INTAKE.md`
- `main.py`, helper scripts, and `run_<taskname>.sh` are implemented and verified
- the collaborator runtime environment contains the prepared task-ready data in the planned layout
- positive and negative evaluation tests behave correctly
- `README.md` and `REPRO_COMMANDS.md` are current
- `CONTEXT.md` is current and reflects the final testing and handoff state
- the task is ready for admin migration handoff
