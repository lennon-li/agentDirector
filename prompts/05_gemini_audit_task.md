# Prompt 05 — Gemini Audit One Task

Read:
- `AGENTS.md`
- `GEMINI.md`
- `agent/PROJECT_BRIEF.md`
- `agent/CURRENT_STATE.md`
- `agent/STOP_RULES.md`
- `agent/TASK_LEDGER.md`
- `agent/DECISION_LOG.md`
- `agent/NEXT_ACTION.md`
- the relevant feature file under `agent/`
- the relevant Spec Kit `spec.md`
- the relevant Spec Kit `plan.md`
- the relevant Spec Kit `tasks.md`
- the latest code diff

Act as whole-codebase auditor.

Review only the implemented task:

[TASK ID AND TASK DESCRIPTION HERE]

Check:
1. Does the change satisfy the task?
2. Does it match the feature spec and acceptance criteria?
3. Does it stay within scope?
4. Did it introduce hidden integration risks?
5. Are tests or validation missing?
6. Did it conflict with existing architecture?
7. Are assumptions recorded and acceptable?
8. Should the human approve, revise, or reject?

Do not implement code.
Do not suggest new features.

Save the audit to:
- `agent/HANDOFF_LOG.md`
- `agent/CURRENT_STATE.md`
- a dedicated audit file if there are blockers, for example `agent/AUDIT_<TASK_ID>_<SHORT_NAME>.md`

Update `agent/TASK_LEDGER.md` to reflect the audit recommendation and set the Audit File column to the audit file path (e.g. `agent/AUDIT_T003_short-slug.md`).

End with the required handoff format from `AGENTS.md`.
