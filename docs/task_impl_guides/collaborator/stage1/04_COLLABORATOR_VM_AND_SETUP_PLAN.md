# Collaborator Stage 1 — Collaborator VM And Setup Plan

## Choose The Working Environment

Pick the actual machine or VM where you will do implementation and testing.

Record in `CONTEXT.md`:

- project name if applicable
- zone if applicable
- VM name or machine name
- OS
- username or access path
- whether remote access was verified this session

If you are using a local workstation rather than a cloud VM, record the equivalent identity clearly.

---

## Decide The Software Provisioning Plan

Answer these questions now:

- what exact software and version does the task require?
- is that software already present on the collaborator machine?
- if not, can it be installed non-destructively?
- does it require a license, login, or manual activation?
- what exact shortcut, launcher, path, or wrapper should the agent rely on?

Rules:

- prefer stable entry points that can later be reproduced by admins
- if a dependency can be installed reliably by CLI, document the exact command path
- if a dependency requires GUI clicks, login, MFA, license activation, or other manual steps, record the handoff item clearly instead of pretending it is automatable
- if the software plan is not credible yet, Stage 1 is not complete

---

## Runtime Contract

Once you choose the collaborator machine, treat it as the canonical execution environment for the task.

Required rules:

- do data inspection, pipeline execution, software checks, and dry runs on the chosen environment whenever possible
- keep the canonical task-ready data there, not only on a separate authoring machine
- record stable identifiers in `CONTEXT.md`
- do not store transient IPs in persistent task docs; if needed for one session, keep them in a task-local `tmp/` folder

If access to the chosen machine is broken, fix access first or record the blocking issue explicitly in `CONTEXT.md`.
