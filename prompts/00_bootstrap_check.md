# Prompt 00 — Bootstrap Check

Run this before any other prompt on a new project.

Read:
- `AGENTS.md`
- `agent/PROJECT_BRIEF.md`
- `agent/CURRENT_STATE.md`
- `agent/STOP_RULES.md`
- `agent/TASK_LEDGER.md`

Check each file for unresolved `TODO` markers.

Report:
1. Which files still contain `TODO` entries
2. Which fields are incomplete (project name, objective, deliverable, stack, build/run/test commands, source layout)
3. Whether it is safe to proceed

Rules:
- If `agent/PROJECT_BRIEF.md` still has TODO in any of: Project Name, Overall Objective, Main Deliverable, or Users / Audience — **stop**. Do not proceed. Ask the Director to fill these in first.
- If `agent/CURRENT_STATE.md` has no current goal — **stop**.
- If `AGENTS.md#project-context` (Stack, Build/Run Commands, Test/Check Commands, Source Layout) is all TODO — **stop**.
- If only minor optional fields are TODO, note them but allow continuation.

Output a checklist:
- [ ] Project Brief complete
- [ ] Current State has a goal
- [ ] AGENTS.md Project Context filled
- [ ] STOP_RULES.md reviewed
- [ ] TASK_LEDGER.md has at least one task defined

If all checks pass:
- State: READY — safe to proceed to `prompts/01_claude_project_familiarization.md`

If any blocking check fails:
- State: BLOCKED — list what the Director must fill in before proceeding
- Do not recommend any agent task
- Do not modify application code

End with the required handoff format from `AGENTS.md`.
