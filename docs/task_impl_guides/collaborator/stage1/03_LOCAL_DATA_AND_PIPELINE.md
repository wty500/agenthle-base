# Collaborator Stage 1 — Local Data And Pipeline

## Raw Data vs Task-Ready Data

Keep the distinction explicit:

- raw data is whatever you received from the original source
- task-ready data is the normalized asset set that the benchmark task will actually use

Stage 1 is responsible for making that mapping explicit in:

- `DATA_INTAKE.md`
- `TASK_INTAKE.md`
- `scripts/DATA_PIPELINE.md`

---

## Canonical Runtime Layout

Canonical collaborator runtime structure:

```text
<runtime_root>/<domain_name>/<task_name>/<variant_name>/
  input/
  output/
  reference/
  output_test_pos/
  output_test_neg/
  software/
```

Directory-role rule:

- `input/` contains agent-visible runtime input only
- `output/` contains the agent's produced output only
- `reference/` contains evaluator-only ground truth
- `output_test_pos/` and `output_test_neg/` contain evaluator fixtures only
- `software/` contains app shortcuts or runtime assets the agent is allowed to use

Do not place planning docs, review artifacts, or repo-side instructions inside these runtime data directories.

---

## Leakage-Prevention Rule

The evaluated agent should only need `input/` and `software/` during execution.

That means:

- do not leave answer keys or judge prompts inside `input/`
- move evaluator-only files into `reference/`
- keep `output_test_pos/` and `output_test_neg/` out of the agent-visible runtime path

Check this boundary explicitly during Stage 1, not only during Stage 2.

---

## `scripts/DATA_PIPELINE.md` Expectations

Record:

- raw source locations
- transformation steps in order
- scripts used and where they run
- naming conventions for variants
- validation checks after each step
- what lands in `input/`, `reference/`, `output_test_pos/`, `output_test_neg/`, and `software/`
- why the chosen positive and negative fixtures are representative

Rules:

- keep the pipeline deterministic where possible
- avoid undocumented manual steps
- if manual work is unavoidable, document exactly what, where, and why
- validate processed data against `TASK_INTAKE.md`, not just file existence
