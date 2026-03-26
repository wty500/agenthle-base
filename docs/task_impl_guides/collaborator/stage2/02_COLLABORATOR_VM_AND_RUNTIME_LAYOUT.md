# Collaborator Stage 2 — Collaborator VM And Runtime Layout

## Runtime Environment Requirement

Collaborator Stage 2 runs against the machine chosen in Stage 1, not against a separate admin inventory VM.

Required rules:

- connect to the chosen machine before running setup, inspection, or test commands
- keep `input/`, `reference/`, and runtime `output/` paths on that machine
- do not treat a successful local-only copy on a different machine as sufficient
- if access is broken, stop and repair it or update `CONTEXT.md` with the blocking issue

Record the stable machine identity in `CONTEXT.md`:

- project
- zone if applicable
- machine or VM name
- access path

Do not store transient IPs in persistent task docs.

---

## Sanity Check Before Testing

Before running Stage 2 tests, verify:

- the collaborator machine matches what is recorded in `CONTEXT.md`
- remote or local access was verified in the current session
- `input/` exists and contains the staged files
- `reference/` exists if evaluation depends on it
- `output_test_pos/` and `output_test_neg/` exist and contain the staged fixtures
- run scripts and helper scripts reference the runtime paths, not stale authoring paths

---

## Runtime Layout Conventions

```text
<runtime_root>/<domain_name>/<task_name>/<variant_name>/
  input/
  output/
  reference/
  output_test_pos/
  output_test_neg/
  software/
```

Data-only rule:

- `input/` stores agent-visible input only
- `software/` stores runtime assets or stable shortcuts only
- `output/` stores the agent's produced output only
- `reference/`, `output_test_pos/`, and `output_test_neg/` remain evaluator-only

Do not place `README.md`, planning docs, `CONTEXT.md`, or review notes inside these runtime directories.
