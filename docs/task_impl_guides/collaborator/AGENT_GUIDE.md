# Collaborator Workflow

> **Who this is for:** contributors who do not have AgentHLE internal database or benchmark-bucket access and will build the task on their own machine or VM.

---

## Goal

Turn real source data plus a rough task description into a complete task folder that:

- has coherent Stage 1 planning artifacts
- has a working Stage 2 implementation
- has been tested on the collaborator VM or workstation
- records enough runtime and migration context for admin handoff
- is ready to submit as a PR to `https://github.com/cua-verse/agenthle-base`

This workflow stops after Stage 2. Do not create Stage 3 validation deliverables unless an admin asks for them explicitly.

---

## Workflow Boundaries

Collaborator tasks do **not** assume access to:

- internal Postgres metadata
- `task_implementations` status writes
- raw submission lookup through admin backend tooling
- benchmark GCS bucket sync such as `gs://agenthle/...`
- admin inventory VM selection

You are responsible for:

- confirming the real source data you were given
- planning the task around that real data
- implementing the task
- testing it on your own VM or workstation
- documenting your runtime environment, software setup, and handoff state
- granting the requested admin access so the task can later be migrated

---

## Read In This Order

1. `stage1/AGENT_GUIDE.md`
2. Scaffold the task folder from `../templates/`
3. Use `../templates/CONTEXT_EXTERNAL.md` as `CONTEXT.md`
4. Finish Stage 1 planning and review
5. `stage2/AGENT_GUIDE.md`
6. Implement and test the task on your collaborator VM or workstation
7. Record PR handoff details and grant the required admin access
8. Open the PR only after the task folder and handoff metadata are complete

---

## Required Deliverables

- `DATA_INTAKE.md`
- `TASK_INTAKE.md`
- `scripts/DATA_PIPELINE.md`
- `CONTEXT.md`
- `PITFALLS.md`
- `main.py`
- `run_<taskname>.sh`
- `README.md`
- `REPRO_COMMANDS.md`

Do not add `REVIEW_REPORT.md` or `FIX_CHANGELOG.md` in the normal collaborator flow.
