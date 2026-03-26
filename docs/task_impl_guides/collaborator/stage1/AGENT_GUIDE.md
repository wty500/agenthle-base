# Collaborator Stage 1 — Intake And Planning

> Read this at the beginning of a collaborator-owned task, before implementation starts.

Use `CHECKLIST.md` in this folder as the Stage 1 checklist source. Paste it into `CONTEXT.md` under `## Check List` and keep it current there.

---

## Python Environment

For Stage 1 local commands, use the current repo environment through `uv run`.

Canonical pattern:

```bash
uv run python ...
```

Use this for:

- local inspection helpers
- data transformation scripts
- review-loop helpers
- benchmark-side scripts that do not depend on internal backend modules

Do not assume access to backend-only environment variables or admin helper scripts.

---

## Goal

Confirm the real source data, choose the collaborator runtime environment, scaffold the task folder, and produce stable planning artifacts grounded in the actual data.

---

## Read In This Order

1. `01_OVERVIEW.md`
2. `02_DATA_SOURCE_AND_ENVIRONMENT.md`
3. `03_LOCAL_DATA_AND_PIPELINE.md`
4. `04_COLLABORATOR_VM_AND_SETUP_PLAN.md`
5. `05_TASK_FOLDER_AND_HANDOFF_STATE.md`
6. `06_PLANNING_REVIEW_AND_EXIT.md`

Use this set as the Stage 1 reading stack rather than as a single long reference file.

---

## Exit Criteria

Stage 1 is complete only when:

- the real source data is identified and documented
- the working collaborator VM or workstation is chosen and reachable
- the software provisioning plan is explicit and credible
- Stage 1 docs are scaffolded and grounded in the actual data
- the data pipeline is specific enough to reproduce the task-ready layout
- positive and negative evaluator fixtures are designed to simulate realistic success and failure cases
- the review loop no longer surfaces unresolved planning issues
- `CONTEXT.md` reflects the current planning and handoff state
