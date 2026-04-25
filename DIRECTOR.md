# DIRECTOR.md

A director-centered workflow guide for managing AI coding agents on this project.

## 1. Your Role

You are the project owner and final decision maker.

You decide:
- what the project is for
- what the deliverable is
- what is out of scope
- when a task is approved
- when to stop
- when to deploy
- whether the agents are creating useful work or unnecessary complexity

Agents can recommend. They do not own purpose.

## 2. Default Workflow

For an existing project with a new feature:

```text
1. Claude understands the project
2. Claude defines the feature
3. Director reviews feature definition
4. Spec Kit creates spec / plan / tasks if feature is non-trivial
5. Director reviews spec / plan / tasks
6. Codex implements one task
7. Gemini audits that task
8. Director approves / revises / rejects
9. Memory is updated
10. Repeat
11. Claude + Gemini final review
12. Director merges/deploys
```

## 3. Required Ending For Every Agent Prompt

Every prompt you give to an agent should end with:

```text
End with the required handoff format from AGENTS.md.
```

This is mandatory for planning, implementation, review/audit, debugging, Spec Kit creation, memory updates, and final review.

## 4. Audit Reports Must Be Saved

After any audit or review, ask the agent to save the result.

The audit should update:

```text
agent/HANDOFF_LOG.md
agent/CURRENT_STATE.md
```

For important audits, create:

```text
agent/AUDIT_<TASK_ID>_<SHORT_NAME>.md
```

A good audit includes:
- approve / revise / reject
- blockers
- risks
- evidence reviewed
- next recommended agent
- next suggested instruction

## 5. When To Use Each Agent

### Use Claude Code when:
- the project needs understanding
- the feature needs definition
- architecture needs thinking
- tasks need to be split
- Spec Kit needs to be created
- final design review is needed

### Use Codex when:
- one task is clearly defined
- implementation should be small
- tests/checks need to be run
- a specific bug needs fixing
- an audit found concrete code issues

### Use Gemini when:
- broad repo context matters
- a task needs independent audit
- implementation may have hidden assumptions
- architecture consistency needs review
- model/pipeline assumptions may be wrong

### Use Copilot / GitHub Agent when:
- you need PR summaries
- issue triage
- GitHub maintenance
- small documentation or repo workflow tasks

## 6. When To Use GitHub Spec Kit

Use Spec Kit when the feature has:
- user-facing behavior
- multiple implementation steps
- acceptance criteria
- validation/testing requirements
- multiple agents involved
- more than a small one-file change

Skip Spec Kit for:
- tiny bug fixes
- one helper function
- text changes
- small CSS/UI tweaks
- quick experiments

## 7. What You Must Manually Review

### Before implementation
Review:
- `agent/PROJECT_BRIEF.md`
- `agent/CURRENT_STATE.md`
- feature definition file
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

### After implementation
Review:
- changed files
- test/check output
- agent handoff
- `agent/VERIFICATION_LOG.md`
- whether the task stayed within scope

### After audit
Review:
- approve/revise/reject recommendation
- risks/open questions
- missing validation
- integration concerns
- whether the audit was saved to project memory

### Before merge/deploy
Review:
- full diff
- acceptance criteria
- final Claude review
- final Gemini audit
- tests/checks
- security/auth/permissions/schema/cost implications

Do not deploy because you are tired. Deploy only because the evidence says it is ready.

## 8. Director Decision Template

After every meaningful handoff, write a decision:

```text
Decision: approve / revise / reject / stop

Reason:
...

Next agent:
Claude / Codex / Gemini / Copilot / Director

Next instruction:
...
```

For important decisions, save it to:

```text
agent/DECISION_LOG.md
```

## 9. Stop Conditions For The Director

Stop when:
- you cannot explain what the agent changed
- the diff is too large to review
- the agent is expanding scope
- the agent is fixing unrelated things
- the agent failed twice on the same issue
- a task touches deployment, secrets, permissions, schema, or user data
- you are tired and tempted to approve without review

## 10. Current-State Discipline

`agent/CURRENT_STATE.md` should always answer:

- What is the current goal?
- What was last completed?
- What is blocked?
- What is the next task?
- Which agent should act next?
- What should not be done?

If this file is stale, update it before continuing.

## 11. Prime Directive

Agents should reduce unfinished work, not create more interesting unfinished work.
