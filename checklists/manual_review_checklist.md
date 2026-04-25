# Manual Review Checklist

## Before Implementation

Review:
- `agent/PROJECT_BRIEF.md`
- `agent/CURRENT_STATE.md`
- relevant feature file under `agent/`
- Spec Kit `spec.md`, if used
- Spec Kit `plan.md`, if used
- Spec Kit `tasks.md`, if used
- `agent/TASK_LEDGER.md`

Ask:
- Is the feature scope correct?
- Is the first task small?
- Is the first task testable?
- Is anything asking Codex to do too much?
- Would I be comfortable reviewing the diff after this task?

## After Implementation

Review:
- changed files
- tests/check output
- agent handoff
- `agent/VERIFICATION_LOG.md`
- whether the task stayed within scope

Ask:
- Did it only do the requested task?
- Are changes surgical?
- Were tests/checks run?
- Are there unexplained failures?
- Is the diff understandable?

## After Audit

Review:
- approve/revise/reject recommendation
- risks/open questions
- missing validation
- integration concerns
- whether the audit was saved to project memory

Ask:
- Do I trust this change?
- Do I understand what changed?
- Is this ready to approve?
- Should Claude re-plan?

## Before Merge/Deploy

Review:
- full diff
- acceptance criteria
- final Claude review
- final Gemini audit
- tests/checks
- security/auth/permissions/schema/cost implications
- `agent/DECISION_LOG.md`
- `agent/RISK_REGISTER.md`
