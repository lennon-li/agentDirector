# Prompt 10 — Rollback a Rejected Task

Use this when an audit recommends reject and the Director approves the rollback.

Read:
- `AGENTS.md`
- `agent/CURRENT_STATE.md`
- `agent/TASK_LEDGER.md`
- `agent/DECISION_LOG.md`
- the audit file for the rejected task (e.g. `agent/AUDIT_<TASK_ID>_<slug>.md`)

## Step 1 — Confirm the rollback target

State:
1. The task ID being rolled back
2. The commit SHA to revert (run `git log --oneline -10` to find it)
3. The files that will be affected
4. Whether any memory files were updated by the rejected task (these must be manually restored)

Do not proceed until the Director confirms the target SHA.

## Step 2 — Revert the code

Run:
```bash
git revert <SHA> --no-edit
```

If the revert has conflicts, stop and report the conflict to the Director. Do not force-resolve.

## Step 3 — Restore memory files if needed

If the rejected task updated any of these, restore them to their pre-task state:
- `agent/CURRENT_STATE.md`
- `agent/TASK_LEDGER.md`
- `agent/HANDOFF_LOG.md`
- `agent/VERIFICATION_LOG.md`
- `agent/ASSUMPTIONS.md`

Do not delete audit files — they are a permanent record.

## Step 4 — Update project memory

Update:
- `agent/TASK_LEDGER.md` — set Status to `REJECTED`, Decision ID to the relevant DECISION-<ID>
- `agent/CURRENT_STATE.md` — set next step to re-plan or stop
- `agent/DECISION_LOG.md` — record the rollback decision using `agent/DECISION_TEMPLATE.md`

## Step 5 — Report

State:
- commit SHA reverted
- files restored
- memory files updated
- whether re-planning is needed before the next implementation attempt

Rules:
- Do not implement a replacement task in this prompt.
- Do not delete audit files.
- If re-planning is needed, the next agent is Claude (main) using `prompts/02_claude_feature_definition.md`.

End with the required handoff format from `AGENTS.md`.
