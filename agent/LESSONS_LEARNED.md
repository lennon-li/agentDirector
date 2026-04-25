# Lessons Learned

Use this file only for reusable lessons that should guide future work.

## Template

### YYYY-MM-DD — Short title
- **Lesson:** What was learned.
- **Trigger:** What caused this lesson to surface.
- **Future rule:** How agents should behave differently going forward.
- **Notes:** Any additional context, exceptions, or caveats.

---

## Example — 2026-01-01 — Always check DECISION_LOG before implementing

- **Lesson:** Codex re-implemented a feature the Director had already rejected because it did not read DECISION_LOG.md first.
- **Trigger:** Gemini caught a duplicate implementation during audit.
- **Future rule:** All worker agents must read DECISION_LOG.md and NEXT_ACTION.md before starting any task.
- **Notes:** This is now enforced in prompts/04_codex_implement_one_task.md and prompts/05_gemini_audit_task.md.
