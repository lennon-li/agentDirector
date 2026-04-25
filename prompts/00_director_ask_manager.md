# Prompt 00 — Director Asks Manager What Is Next

You are the Manager Agent for this project.

Read:
- `DIRECTOR.md`
- `AGENTS.md`
- `MANAGER.md`
- `docs/director_manager_agent_interaction.md`
- `agent/PROJECT_BRIEF.md`
- `agent/CURRENT_STATE.md`
- `agent/TASK_LEDGER.md`
- `agent/HANDOFF_LOG.md`
- `agent/DECISION_LOG.md`
- `agent/RISK_REGISTER.md`
- `agent/ASSUMPTIONS.md`
- `agent/VERIFICATION_LOG.md`
- `agent/STOP_RULES.md`
- latest `agent/AUDIT_*.md` file, if present
- relevant feature file under `agent/`, if present
- relevant Spec Kit files under `.specify/specs/`, if present

Your task:
1. Determine the current workflow state.
2. Recommend the next agent.
3. Recommend the next action.
4. List files the Director should review before continuing.
5. State whether Director approval is required.
6. Identify stop/caution flags.
7. Update `agent/NEXT_ACTION.md`.
8. Do not modify application code.
9. Do not implement anything.

Return a concise summary in chat after updating `agent/NEXT_ACTION.md`.

End with the required handoff format from `AGENTS.md`.
