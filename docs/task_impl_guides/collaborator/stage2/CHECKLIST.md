# Stage 2 Checklist

Copy this checklist into `CONTEXT.md` under `## Check List` while the task is in Stage 2, and keep it updated in place.

- [ ] Collaborator Stage 2 guide read
- [ ] `main.py`, helper scripts, and `run_<taskname>.sh` implemented
- [ ] Agent-facing prompt or task description reviewed for leakage of evaluation, reference, or judge-only details
- [ ] Runtime `input/` reviewed to confirm it contains no answer key, reference output, or hidden scoring details
- [ ] `start()` and test commands reviewed to confirm evaluator fixtures are treated as read-only and the output directory is not cleared during setup
- [ ] `README.md` and `REPRO_COMMANDS.md` written
- [ ] `start()` setup test passing on the collaborator runtime environment
- [ ] Pos/neg evaluation tests passing on the collaborator runtime environment
- [ ] Handoff notes, access grant status, and migration context recorded in `CONTEXT.md`
