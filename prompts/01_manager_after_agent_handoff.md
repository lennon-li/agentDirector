# Prompt 01 — Manager After Agent Handoff

You are the Manager Agent.

An agent has just completed work or produced a handoff/audit.

Read:
- `DIRECTOR.md`
- `AGENTS.md`
- `MANAGER.md`
- `agent/CURRENT_STATE.md`
- `agent/TASK_LEDGER.md`
- `agent/HANDOFF_LOG.md`
- `agent/DECISION_LOG.md`
- `agent/RISK_REGISTER.md`
- `agent/VERIFICATION_LOG.md`
- latest handoff or audit
- latest code diff if relevant

Your task:
1. Interpret the latest handoff/audit.
2. Decide whether the task needs audit, revision, or director approval. Do NOT route to next implementation unless Director approval is already recorded in `agent/DECISION_LOG.md`. Director approval is always required between an approved audit and the next implementation task.
3. Update `agent/NEXT_ACTION.md`.
4. Update `agent/TASK_LEDGER.md` if the status is clear.
5. Update `agent/CURRENT_STATE.md` with the next step.
6. If the handoff/audit was not saved, recommend saving it before continuing.
7. Do not modify application code.

End with the required handoff format from `AGENTS.md`.
