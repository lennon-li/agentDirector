# Spec Kit Review Checklist

Review these files before implementation:

- `.specify/specs/<feature>/spec.md`
- `.specify/specs/<feature>/plan.md`
- `.specify/specs/<feature>/tasks.md`

## spec.md

Check:
- The feature still says what you actually want.
- User stories are clear.
- Acceptance criteria are testable.
- Out-of-scope items are explicit.
- Predictive, experimental, or uncertain outputs are clearly labeled.

## plan.md

Check:
- No new dependencies unless necessary.
- No redesign of unrelated systems.
- The change is additive when possible.
- Error handling is planned.
- Testing/validation approach is realistic.
- Director approval gates are respected.

## tasks.md

Check:
- The first implementation task is small.
- Tasks are ordered by dependency.
- Tests/validation tasks exist.
- No task sneaks in too much work.
- Codex can complete one task without touching unrelated areas.
- No task range asks one agent to implement too much.
