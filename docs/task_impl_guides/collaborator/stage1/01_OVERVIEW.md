# Collaborator Stage 1 — Overview

## Goal

Confirm the real source data, choose the collaborator runtime environment, scaffold the task folder, and produce stable planning artifacts grounded in the actual data.

---

## Overview

1. confirm the real source data and the current working copy
2. decide the canonical task identity and variant layout
3. decide the collaborator VM or workstation that will be the execution environment
4. scaffold the task folder and start the living docs
5. inspect, normalize, and validate the raw data
6. organize the task-ready data into the canonical runtime layout
7. decide the software provisioning plan, including any admin handoff items
8. run the Stage 1 planning review loop and capture stable takeaways in `CONTEXT.md` and `PITFALLS.md`
9. update the Stage 1 docs based on confirmed review feedback
10. finish Stage 1 planning and record the handoff state in `CONTEXT.md`

---

## Domain, Task, And Variant

Stage 1 must make the following explicit for every task:

- `domain_name`
- `task_name`
- `variant_name` or the rule that enumerates variants

Stage 1 must also make the runtime asset layout explicit:

- collaborator runtime path: `<domain_name>/<task_name>/<variant_name>/...`
- repo task path: `tasks/<domain_name>/<task_name>/...`

Keep these two layouts aligned in `TASK_INTAKE.md`, `scripts/DATA_PIPELINE.md`, and `CONTEXT.md`.
