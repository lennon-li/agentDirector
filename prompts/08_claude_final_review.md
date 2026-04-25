# Prompt 08 — Claude Final Review

Read:
- `AGENTS.md`
- `CLAUDE.md`
- `agent/PROJECT_BRIEF.md`
- `agent/CURRENT_STATE.md`
- `agent/HANDOFF_LOG.md`
- `agent/TASK_LEDGER.md`
- `agent/STOP_RULES.md`
- relevant feature file
- relevant Spec Kit `spec.md`, `plan.md`, and `tasks.md`
- full code diff for this feature

Act as final architecture/design reviewer.

Check:
1. Did we satisfy the original feature objective?
2. Did we stay within scope?
3. Are acceptance criteria met?
4. Are tests/validation sufficient?
5. Is the implementation unnecessarily complex?
6. Are there hidden maintainability or architecture risks?
7. Is anything risky before merge/deploy?
8. What should be documented in `LESSONS_LEARNED.md`?

Do not implement code.

Return:
- approve / revise / reject recommendation
- specific reasons
- any required director review items

Save final review summary to `agent/HANDOFF_LOG.md`.

End with the required handoff format from `AGENTS.md`.
