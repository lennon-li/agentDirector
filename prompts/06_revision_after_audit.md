# Prompt 06 — Revision After Audit

Read:
- `AGENTS.md`
- relevant agent-specific instruction file
- `agent/CURRENT_STATE.md`
- `agent/STOP_RULES.md`
- `agent/TASK_LEDGER.md`
- the relevant feature file
- the relevant Spec Kit files
- the audit file or audit report
- the current code diff

Before revising, verify Director approval:

Check `agent/DECISION_LOG.md` or `agent/NEXT_ACTION.md` for a recorded Director decision approving this revision.
If no Director approval is recorded, stop immediately and report to the Director. Do not implement.

Task:
Revise only the previously implemented task:

[TASK ID AND TASK DESCRIPTION HERE]

Address only these audit findings:

[PASTE FINDINGS HERE]

Rules:
- Do not implement later tasks.
- Do not add unrelated improvements.
- Do not refactor unrelated code.
- Make the smallest safe patch.
- Update verification evidence.
- Update `agent/TASK_LEDGER.md` to `NEEDS_AUDIT` when done.

End with the required handoff format from `AGENTS.md`.
