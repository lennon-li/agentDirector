# Prompt 04 — Codex Implement One Task

Read:
- `AGENTS.md`
- `.codex/instructions.md`
- `agent/CURRENT_STATE.md`
- `agent/STOP_RULES.md`
- `agent/TASK_LEDGER.md`
- `agent/DECISION_LOG.md`
- `agent/NEXT_ACTION.md`
- the relevant feature file under `agent/`
- the relevant Spec Kit `spec.md`
- the relevant Spec Kit `plan.md`
- the relevant Spec Kit `tasks.md`

Before implementing, verify Director approval:

Check `agent/DECISION_LOG.md` or `agent/NEXT_ACTION.md` for a recorded Director decision approving this specific task.
If no Director approval is recorded, stop immediately and report to the Director. Do not implement.

Implement only this task:

[TASK ID AND TASK DESCRIPTION HERE]

Before editing, state:
1. the goal of this task
2. the root cause or implementation need
3. the files you expect to touch
4. how you will verify it

Rules:
- Do not implement later tasks.
- Do not modify unrelated files unless this task explicitly requires it.
- Do not refactor unrelated code.
- Do not add dependencies unless this task explicitly requires it.
- Make the smallest safe patch.
- Add or update only tests needed for this task if the project has a test structure.
- Run relevant tests/checks if possible.
- Update `agent/TASK_LEDGER.md` status to `NEEDS_AUDIT` when done. Leave the Audit File column as `—`.
- Update `agent/VERIFICATION_LOG.md` with evidence.
- After two failed attempts, stop and summarize the blocker.

End with the required handoff format from `AGENTS.md`.
