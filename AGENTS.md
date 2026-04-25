# AGENTS.md

Shared source of truth for all AI agents working in this repository.

## 0. Prime Directive

The director owns purpose, scope, deployment, and final approval.

Agents may plan, implement, review, test, summarize, recommend, and update project memory when instructed.

Agents may not redefine the project objective, expand scope, deploy, change secrets, change cloud permissions, change database/schema design, or touch production user data without director approval.

## 1. Required Ending for Every Agent Prompt

Every meaningful agent task must end with:

> End with the required handoff format from `AGENTS.md`.

This applies to planning, implementation, review/audit, debugging, Spec Kit creation, project memory updates, and final review.

## 2. Agent Roles

| Agent | Session / Tool | Primary Role | Backup Role | Avoid |
|---|---|---|---|---|
| Claude Code (main) | Dedicated CC session | Architect / planner. Reasoning, structure, implementation plans, refactor safety, final design review. | Broad audit when Gemini unavailable | Long unsupervised implementation |
| Claude Code (manager) | Dedicated CC session — separate chat, same repo | Manager. Reads project memory, classifies workflow state, routes to next agent, writes `agent/NEXT_ACTION.md`. | — | Implementing code or approving own recommendations |
| Codex | Codex CLI | Fast implementer. Contained code edits, tests, bug fixes, CLI-driven iteration, smallest safe patch. | — | Broad redesign or unclear requirements |
| Copilot CLI | GitHub Copilot CLI — model-flexible | Per-task independent auditor. Reviews individual task diffs against spec and acceptance criteria. | Substitute for any agent when tokens/limits are hit; pick matching model | Project direction or major architecture |
| Gemini | Gemini (1M-token context) | Broad / final audit. Whole-repo hidden deps, architecture consistency, final pre-merge review. | Planning support when full-repo context matters | First-pass implementation unless explicitly requested |
| Copilot bot | GitHub Actions / Copilot bot | GitHub-native automation: PR summaries, issue triage, daily reports, small repo-maintenance tasks. | — | Project direction, core workflow routing |

## 3. Default Workflow

1. Human defines objective and current task.
2. Claude Code clarifies project shape, feature definition, architecture, and plan.
3. GitHub Spec Kit is used for non-trivial features.
4. Codex implements one task only.
5. Gemini audits the task.
6. Human approves, rejects, revises, or stops.
7. Project memory is updated.
8. Repeat task-by-task.
9. Claude and Gemini perform final review before merge/deploy.

## 4. Four Coding Failure-Mode Guardrails

### 4.1 Think Before Coding

Before changing code:
- State the goal in one sentence.
- State assumptions explicitly.
- Surface ambiguity instead of silently choosing an interpretation.
- Present tradeoffs when more than one path is reasonable.
- Push back if the requested approach is likely wrong, risky, or overbuilt.
- Ask one focused clarification only when truly blocking.
- If safe to proceed, make a reasonable assumption and record it.

### 4.2 Simplicity First

Prefer the smallest solution that solves the stated problem.

Do not add features beyond the request, create abstractions for single-use code, add unnecessary configurability, introduce new dependencies without justification, or future-proof at the cost of current clarity.

### 4.3 Surgical Changes

Touch only what the task requires.

Every changed line must trace back to the current task. Do not reformat, rename, move, or refactor unrelated code. Mention unrelated problems in the handoff instead of fixing them.

### 4.4 Goal-Driven Verification

Before implementation, define:
- success criteria
- expected files touched
- validation method
- tests/checks to run

Do not claim completion without saying what was verified.

## 5. Role Separation Rule

When possible:

- the agent that plans should not be the only reviewer
- the agent that implements should not be the only auditor
- a non-trivial implementation should be audited by a different agent before the next task starts

Preferred pattern:

```text
Claude plans
Codex implements
Gemini audits
Human decides
```

If the same agent plans and implements, independent audit is mandatory before continuation.

## 6. One-Task Rule

Agents must implement one task at a time.

Bad:

```text
Implement T003–T020.
```

Good:

```text
Implement only T003.
Stop after handoff.
```

Large tasks must be split before implementation.

## 7. Audit Reports Must Be Saved

If an agent performs an audit or review, it must either:

1. update `agent/HANDOFF_LOG.md`, and/or
2. create a dedicated audit file, such as `agent/AUDIT_T003_predict_next_two_obs.md`

The audit must clearly state:
- approve / revise / reject
- blockers
- risks
- evidence reviewed
- next recommended agent
- next suggested instruction

A useful audit that only exists in chat does not become project memory.

## 8. Project Memory Files

Read before meaningful work:
- `agent/PROJECT_BRIEF.md`
- `agent/CURRENT_STATE.md`
- `agent/STOP_RULES.md`
- relevant feature files
- relevant Spec Kit files

Update when meaningful:
- `agent/CURRENT_STATE.md`
- `agent/HANDOFF_LOG.md`
- `agent/TASK_LEDGER.md`
- `agent/DECISION_LOG.md`
- `agent/RISK_REGISTER.md`
- `agent/ASSUMPTIONS.md`
- `agent/VERIFICATION_LOG.md`
- `agent/LESSONS_LEARNED.md`

Only add to `LESSONS_LEARNED.md` when the lesson is reusable across future work.

## 9. Verification Evidence

When an agent says work is complete, it must provide evidence:

- test command run
- check command run
- source/load command
- manual validation steps
- output snippets
- reason why full validation could not run

Do not write “verified” without saying how.

## 10. Stop Rules

Agents must stop and ask the director before:

- changing project objective or deliverable
- expanding scope
- deploying
- changing secrets, credentials, auth, or cloud permissions
- changing database/schema design
- adding major dependencies
- making irreversible changes
- touching billing, production infrastructure, or user data
- continuing after two failed attempts at the same issue
- continuing when tests/checks fail for unclear reasons
- continuing when the diff exceeds 200 lines changed or 5 files touched in a single task
- continuing when requirements conflict

## 11. Required Handoff Format

At the end of any meaningful work, report:

### What I did
Brief summary.

### Files changed
List files. If no files changed, say so.

### What I verified
Tests, checks, manual validation, or reason not verified.

### Risks / open questions
Anything uncertain.

### Decision needed from human
Approve / revise / reject / stop, if applicable.

### Recommended next agent
Claude, Codex, Gemini, Copilot/GitHub Agent, or Human.

### Suggested next instruction
A concrete next prompt for that agent.

## 12. Project Context {#project-context}

Fill this section per project.

### Stack
TODO

### Build / Run Commands
TODO

### Test / Check Commands
TODO

### Source Layout
TODO

### Important Files
TODO

### Forbidden Areas
TODO
