# Prompt 11 — Manager Sanity Check (Independent Verification)

Run this every 5 Manager routings, or any time a Manager recommendation feels wrong.

You are Gemini acting as an independent verifier. You are NOT the Manager. Do not defer to what the Manager said — form your own view from the raw project memory.

Read:
- `AGENTS.md`
- `MANAGER.md`
- `agent/PROJECT_BRIEF.md`
- `agent/CURRENT_STATE.md`
- `agent/TASK_LEDGER.md`
- `agent/HANDOFF_LOG.md`
- `agent/DECISION_LOG.md`
- `agent/RISK_REGISTER.md`
- `agent/VERIFICATION_LOG.md`
- `agent/NEXT_ACTION.md` (the Manager's latest recommendation)
- latest `agent/AUDIT_*.md` file, if present

Your task:

1. Independently classify the current workflow state using the states defined in `MANAGER.md` §3.
2. Compare your classification to the Manager's classification in `agent/NEXT_ACTION.md`.
3. Check whether the Manager's recommended next agent and action are consistent with routing rules in `MANAGER.md` §4.
4. Check whether any stop conditions in `MANAGER.md` §5 are currently met but were not flagged.
5. Check whether `agent/CURRENT_STATE.md` and `agent/TASK_LEDGER.md` are consistent with each other.
6. Check whether the last implementation was audited before the Manager routed to the next task.

Report:

### Manager Classification
What the Manager said the state is.

### Your Independent Classification
What you believe the state is, based solely on project memory.

### Agreement
Agree / Disagree / Partially agree

### Discrepancies Found
List any mismatches, missed stop conditions, or inconsistent memory files.

### Recommendation
- CONFIRM: Manager recommendation is sound — Director may proceed.
- REVISE: Manager recommendation has issues — describe what should change.
- STOP: A stop condition is met that the Manager missed — do not proceed.

Rules:
- Do not modify application code.
- Do not implement anything.
- Do not update `agent/NEXT_ACTION.md` — that is the Manager's file.
- Save this sanity check to `agent/SANITY_CHECK_<YYYY-MM-DD>.md`.

End with the required handoff format from `AGENTS.md`.
