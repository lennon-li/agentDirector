# Risk Register

Track unresolved risks and mitigation plans.

| Risk ID | Risk | Severity | Likelihood | Mitigation | Owner | Status | Notes |
|---|---|---|---|---|---|---|---|
| R001 | Example: schema change breaks existing queries | High | Low | Review all queries before schema change | Director | Open | Add any context the agent wants to record here |
| R002 | The new orchestrator's live Claude Manager flow has not been exercised end-to-end yet because running it would update existing `agent\*.md` files and requires a configured `ANTHROPIC_API_KEY`. | Medium | Medium | Configure `.env`, then run `python -m orchestrator.director_loop --dry-run --once` in a controlled follow-up and inspect the resulting memory updates. | Director | Open | Implementation and read-only helper validation passed; live write path still needs confirmation. |
| R003 | `orchestrator\requirements.txt` and `orchestrator\.env.example` were placed under `orchestrator\` per director instruction, which differs from the original plan's repo-root placement. | Low | Medium | Decide whether the override is now the intended standard; if not, reconcile the plan and file placement in a later approved task. | Director | Open | Current implementation matches the explicit implementation instruction rather than the earlier draft plan. |
