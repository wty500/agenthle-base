# Collaborator Stage 2 — `main.py` And Evaluation

## `main.py` Principles

1. `start()` does not open software.
2. `start()` does not copy input into output.
3. `start()` only installs eval-required packages, performs light environment checks, and ensures the runtime output directory exists.
4. `start()` does not perform database queries or GCS sync.
5. `start()` does not attempt GUI-heavy, licensed, login-gated, or manually activated installs unless that manual step is already documented as a handoff item.
6. `evaluate()` assumes reference data already exists in the runtime layout before evaluation starts.
7. Eval scripts print JSON to stdout and debug logs to stderr.
8. `reference/` is evaluator-only data. Do not treat it as agent-readable input.
9. `output_test_pos/` and `output_test_neg/` are evaluator fixtures, not runtime input for the evaluated agent.
10. Before Stage 2 is considered implementation-complete, explicitly review the agent-facing prompt and runtime `input/` contents for leakage of evaluator-only details.

---

## Task Config Pattern

```python
from dataclasses import dataclass
from pathlib import Path
from tasks.common_config import GeneralTaskConfig

@dataclass
class MyTaskConfig(GeneralTaskConfig):
    TASK_CATEGORY: str = "manufacturing"
    TASK_TAG: str = ""

    @property
    def input_dir(self) -> str:
        return rf"{self.task_dir}\input"

    @property
    def output_file(self) -> str:
        return rf"{self.remote_output_dir}\result.txt"

    @property
    def reference_file(self) -> str:
        return rf"{self.reference_dir}\reference.txt"
```

Keep metadata aligned with the runtime layout that Stage 1 prepared.

---

## `start()` For Setup

Stage 2 begins only after task-ready data has already been staged onto the collaborator machine.

```python
@cb.setup_task(split="train")
async def start(task_cfg, session: cb.DesktopSession):
    meta = task_cfg.metadata
    outdir = meta["remote_output_dir"]

    await session.run_command("pip install trimesh numpy")
    await session.makedirs(outdir)
```

Rules:

- do not hide data staging inside `start()`
- do not clear evaluator fixtures during setup
- if required software still needs manual installation, record that cleanly in `README.md`, `PITFALLS.md`, and `CONTEXT.md`

---

## `evaluate()` For Scoring

Reference data is already present in the runtime layout before evaluation starts.

Keep verifier logic in task-local files under `scripts/`, and upload or invoke only the pieces actually needed at runtime.

```python
SCRIPTS_DIR = Path(__file__).parent / "scripts"

@cb.evaluate_task(split="train")
async def evaluate(task_cfg, session: cb.DesktopSession) -> list[float]:
    meta = task_cfg.metadata
    ref_file = meta["reference_file"]
    output_file = meta["output_file"]
    ...
```

Preferred scoring order:

1. exact file match or hash comparison
2. structured diff
3. metric comparison with tolerances
4. LLM judge only as a last resort

Treat prompt and `input/` leakage review as a required Stage 2 step, not as an optional best practice.
