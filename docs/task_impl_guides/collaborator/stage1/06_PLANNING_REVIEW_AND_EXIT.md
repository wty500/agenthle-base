# Collaborator Stage 1 — Planning, Review, And Exit

## Stage 1 Planning Docs Expectations

Use the templates as the source of truth for field-by-field structure.

Minimum expectations:

- `DATA_INTAKE.md` is grounded in the real source data
- `TASK_INTAKE.md` describes the actual workflow, software plan, benchmark-ready input, expected output, and evaluation contract
- `scripts/DATA_PIPELINE.md` explains how raw data becomes the canonical runtime structure
- `scripts/DATA_PIPELINE.md` documents where each step runs
- `output_test_pos/` and `output_test_neg/` are realistic, representative, and aligned with the planned evaluator

Use `PITFALLS.md` for recurring mistakes, fragile assumptions, and review takeaways that should not be buried inside the intake templates.

---

## Run The Review Loop

Stage 1 still requires review of the task description itself.

```bash
curl -N https://agenthle-backend-preview-nlsao4fgla-uc.a.run.app/agent/evaluate \
  -H "Authorization: Bearer ${AGENTHLE_REVIEW_BEARER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "taskDescription": ""
}'
```

Do not commit bearer tokens into the repo.

Record stable takeaways in:

- `CONTEXT.md`
- `PITFALLS.md`

After the review returns:

- update the Stage 1 planning docs when the review reveals a real gap, ambiguity, or mismatch
- do not apply feedback mechanically; first confirm whether the reported issue is actually real in the current files

---

## Exit Criteria

Stage 1 is complete only when:

- the real source data and current working copy are identified
- the working collaborator machine is chosen and reachable
- the software provisioning plan is explicit and credible
- `DATA_INTAKE.md` matches the real source data
- `TASK_INTAKE.md` is concrete and reviewable
- `scripts/DATA_PIPELINE.md` is specific enough to trust
- the positive and negative fixtures are designed to simulate realistic success and failure cases
- the review loop no longer surfaces unresolved planning issues
- `CONTEXT.md` reflects the current planning state and handoff state
