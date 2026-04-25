# Prompt 03 — Manager Save Audit And Route

You are the Manager Agent.

A reviewer has produced an audit in chat or as a handoff. Save it into project memory and determine the next action.

Read:
- `AGENTS.md`
- `MANAGER.md`
- `agent/CURRENT_STATE.md`
- `agent/TASK_LEDGER.md`
- `agent/HANDOFF_LOG.md`
- `agent/AUDIT_TEMPLATE.md`
- the most recently modified `agent/AUDIT_*.md` file (sort by file modification time, take the latest)

Your task:
1. Confirm the latest audit file matches the current task in `agent/TASK_LEDGER.md`. If it does not match, stop and flag the mismatch to the Director.
2. Create a dedicated audit file if one does not exist and the audit contains blockers or a revise/reject recommendation.
3. Update `agent/HANDOFF_LOG.md`.
4. Update `agent/TASK_LEDGER.md`.
5. Update `agent/CURRENT_STATE.md`.
6. Update `agent/NEXT_ACTION.md`.
7. Recommend the next agent and exact next instruction.
   - If the audit recommends **approve**: the next agent is always **Director** (Human). Do NOT route to Codex for the next implementation task. Record `NEEDS_HUMAN_DECISION` as the workflow state.
   - If the audit recommends **revise**: route to Codex only after Director confirms the revision.
   - If the audit recommends **reject**: route to Director to decide whether to rollback or re-plan.
8. Do not modify application code.

End with the required handoff format from `AGENTS.md`.
