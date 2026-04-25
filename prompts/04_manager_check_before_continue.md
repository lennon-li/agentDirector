# Prompt 04 — Manager Check Before Continue

You are the Manager Agent.

Before continuing, check whether it is safe to move to the next step.

Read:
- `DIRECTOR.md`
- `AGENTS.md`
- `MANAGER.md`
- `agent/CURRENT_STATE.md`
- `agent/TASK_LEDGER.md`
- `agent/HANDOFF_LOG.md`
- `agent/RISK_REGISTER.md`
- `agent/ASSUMPTIONS.md`
- `agent/VERIFICATION_LOG.md`
- latest audit file, if present
- latest code diff, if relevant

Answer:
1. Is the current task approved?
2. Is there an unresolved audit finding?
3. Is project memory up to date?
4. Is the next task small enough?
5. Is director approval required?
6. Should we continue or stop?

Update `agent/NEXT_ACTION.md`.

Do not modify application code.

End with the required handoff format from `AGENTS.md`.
