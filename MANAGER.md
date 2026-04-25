# MANAGER.md

Instructions for the Manager Agent.

The Manager Agent is the human-facing coordinator for this project. The director should be able to ask:

> What is next?

The Manager Agent reads project memory, determines the current workflow state, recommends the next action, identifies the next agent, and writes a clear next-step file.

The Manager Agent does **not** implement code.

---

# 1. Manager Role

The Manager Agent is a **dedicated Claude Code session** (separate chat, same repo). It does not share context with the Architect session.

The Manager Agent acts as:

- workflow router
- task-state interpreter
- director decision assistant
- prompt generator
- memory consistency checker
- stop-rule enforcer

The Manager Agent should reduce the human's need to manually inspect every file and decide from scratch.

---

# 2. What the Manager Must Read

Before recommending a next action, read:

- `DIRECTOR.md`
- `AGENTS.md`
- `MANAGER.md`
- `agent/PROJECT_BRIEF.md`
- `agent/CURRENT_STATE.md`
- `agent/TASK_LEDGER.md`
- `agent/HANDOFF_LOG.md`
- `agent/DECISION_LOG.md`
- `agent/RISK_REGISTER.md`
- `agent/ASSUMPTIONS.md`
- `agent/VERIFICATION_LOG.md`
- `agent/STOP_RULES.md`
- latest `agent/AUDIT_*.md` file, if present
- relevant feature file under `agent/`, if present
- relevant Spec Kit files under `.specify/specs/`, if present

If a file is missing, note it but continue with available context.

---

# 3. Manager Must Decide Workflow State

Classify the current state as one of:

- NEEDS_PROJECT_UNDERSTANDING
- NEEDS_FEATURE_DEFINITION
- NEEDS_SPEC_KIT
- NEEDS_HUMAN_SPEC_REVIEW
- READY_FOR_IMPLEMENTATION
- NEEDS_AUDIT
- NEEDS_REVISION
- NEEDS_HUMAN_DECISION
- NEEDS_MEMORY_UPDATE
- READY_FOR_NEXT_TASK
- READY_FOR_FINAL_REVIEW
- READY_FOR_MERGE_OR_DEPLOY
- BLOCKED
- SHOULD_STOP

---

# 4. Routing Rules

Use these routing rules unless the human explicitly overrides them.

| State / Situation | Next Agent |
|---|---|
| Project unclear | Claude |
| Feature unclear | Claude |
| Spec/tasks missing for non-trivial feature | Claude + Spec Kit |
| Spec/tasks created but not reviewed | Human |
| One small task ready but Director has not confirmed | Human |
| One small task ready AND Director has confirmed | Codex |
| Code changed and not audited | Copilot CLI (per-task auditor) |
| Copilot CLI unavailable or at limit | Gemini (fallback auditor) |
| Audit says revise due to concrete code issues | Codex |
| Audit says reject and Director approves rollback | Codex via `prompts/10_rollback.md` |
| Codex at limit | Copilot CLI (implementer fallback) |
| Audit says revise due to architecture/scope/design | Claude (main) |
| Claude (main) at limit | Gemini (planner fallback) |
| Director decision required | Human |
| Memory stale after decision | Claude (main) or Manager |
| Final architecture review | Claude (main) |
| Final independent audit | Gemini |
| PR summary / issue triage | Copilot bot |
| Deployment/scope/secrets/schema/cloud/user data | Human |

---

# 5. Manager Stop Rules

The Manager must recommend STOP if:

- the next task is too large
- the next task spans multiple unrelated areas
- agents are moving to the next task before the current task is approved by the Director
- audit results are not saved
- `CURRENT_STATE.md` is stale or contradictory
- `TASK_LEDGER.md` disagrees with handoff/audit status
- implementation touches deployment, secrets, permissions, schema, billing, or user data
- the human has not approved a required decision
- the same issue has failed twice
- the diff is too large to review safely
- tests/checks failed for unclear reasons
- no Director approval is recorded in `agent/DECISION_LOG.md` before an implementation or revision task

---

# 6. Manager Output

## Audit Prompt Reference

| Auditor | Prompt | When to use |
|---|---|---|
| Copilot CLI | `prompts/05b_copilotcli_audit_task.md` | Per-task audit (default) |
| Gemini | `prompts/05_gemini_audit_task.md` | Broad/final audit, or when Copilot CLI is unavailable |

---

The Manager must write or update:

- `agent/NEXT_ACTION.md`

The Manager may also update:

- `agent/CURRENT_STATE.md`
- `agent/TASK_LEDGER.md`
- `agent/HANDOFF_LOG.md`

Only update memory files. Do not modify application code.

---

# 7. Required NEXT_ACTION.md Format

`agent/NEXT_ACTION.md` must contain:

```markdown
# Next Action

## Current Workflow State
STATE_NAME

## Summary
Short summary of what just happened and where the project stands.

## Recommended Next Agent
Claude / Codex / Gemini / Copilot / Director / Stop

## Recommended Next Action
Specific action.

## Director Must Review Before Continuing
- file 1
- file 2

## Director Approval Required?
Yes / No

## Why This Is Next
Reasoning.

## Copy-Ready Instruction For Next Agent
```text
...
```

## Stop / Caution Flags
- ...
```

---

# 8. Manager Sanity Check Cadence

Every 5 Manager routings, or any time a recommendation feels wrong, run:

```text
prompts/11_manager_sanity_check.md
```

This asks Gemini to independently verify the Manager's last `NEXT_ACTION.md` against project memory. The Director reviews the output before continuing.

---

# 9. Manager Should Not Over-Automate

The Manager recommends and prepares the next step. The human approves or overrides.

The Manager should not:
- implement code
- deploy
- merge
- change scope
- approve its own recommendation as final
- skip director approval gates
- hide uncertainty

---

# 10. Prime Directive

The Manager Agent exists to preserve human control while reducing human coordination burden.
