# Prompt 02 — Claude Feature Definition

Now I want to add this functionality:

[DESCRIBE FEATURE HERE]

Act as architect/planner.

Read:
- `AGENTS.md`
- `CLAUDE.md`
- `agent/PROJECT_BRIEF.md`
- `agent/CURRENT_STATE.md`
- `agent/STOP_RULES.md`

Create or update a feature definition file under `agent/`, for example:

`agent/FEATURE_<NAME>.md`

Include:

1. Feature description
2. Why this feature matters
3. User workflow
4. Acceptance criteria
5. Out-of-scope items
6. Risks / unclear areas
7. Assumptions
8. Smallest useful first milestone
9. Recommendation on whether to use GitHub Spec Kit

Update:
- `agent/CURRENT_STATE.md`
- `agent/RISK_REGISTER.md`, if risks are identified
- `agent/ASSUMPTIONS.md`, if assumptions are made

Do not implement code.
Do not expand scope.
If anything is unclear, make a reasonable assumption and record it, or ask one focused blocking question.

End with the required handoff format from `AGENTS.md`.
