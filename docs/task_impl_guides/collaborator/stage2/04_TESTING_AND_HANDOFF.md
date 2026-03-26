# Collaborator Stage 2 — Testing And Handoff

## Testing Strategy

### Setup and evaluate separately

| Phase | What to test | How |
|---|---|---|
| setup | `start()` installs dependencies and prepares runtime directories only | `--setup-only` |
| evaluate | `evaluate()` scores positive and negative outputs correctly | `--eval` with `REMOTE_OUTPUT_DIR` |

### Required output directories per variant

| Directory | Contents | Expected score |
|---|---|---|
| `output_test_pos/` | known-correct output | about `1.0` |
| `output_test_neg/` | clearly wrong output | about `0.0` |

### Run script shape

Each task must commit `run_<taskname>.sh`.

```bash
#!/bin/bash

export TASK_NAME="<task_name>"
export LOCAL_TASK_DIR="./tasks/<category>/<task_name>"
export REMOTE_OUTPUT_DIR="${REMOTE_OUTPUT_DIR:-output}"

uv run python -m cua_bench.batch.solver "$LOCAL_TASK_DIR" \
  --eval \
  --dump \
  --output-dir "./trycua/cua-bench/$TASK_NAME"
```

### Commands to run

```bash
uv run python -m cua_bench.batch.solver ./tasks/<category>/<task_name> \
  --setup-only --output-dir ./trycua/cua-bench/<task_name>

REMOTE_OUTPUT_DIR=output_test_pos bash tasks/<category>/<task_name>/run_<taskname>.sh
REMOTE_OUTPUT_DIR=output_test_neg bash tasks/<category>/<task_name>/run_<taskname>.sh
```

Save the exact commands in `REPRO_COMMANDS.md`.

---

## Handoff Requirements

Before declaring Stage 2 complete, record in `CONTEXT.md`:

- final testing state
- unresolved blockers or manual install steps
- runtime machine identity and important paths
- what admins must reproduce during migration
- whether access was granted to the requested admin user and service account
- PR URL once opened

Treat `output_test_pos/` and `output_test_neg/` as read-only evaluator fixtures, not as ordinary runtime output directories.
