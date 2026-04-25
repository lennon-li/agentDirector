# Manager Routing Checklist

Use this to verify the Manager Agent's recommendation.

## Before accepting the manager recommendation

Check:

- Does `CURRENT_STATE.md` match the latest handoff/audit?
- Does `TASK_LEDGER.md` show the right status?
- Did the last implementation get audited?
- Did the audit get saved?
- Is the next task one task only?
- Is the recommended next agent appropriate?
- Is director approval required?
- Are there stop/caution flags?

## Common routing

| Situation | Correct next move |
|---|---|
| Code changed but not audited | Gemini audit |
| Audit says revise concrete code bugs | Codex revision |
| Audit says design/scope issue | Claude re-plan |
| Task approved but memory stale | Manager/Claude update memory |
| Spec created but not reviewed | Director review |
| Task too large | Claude split task |
| Deployment/security/schema/cost issue | Director decision |
