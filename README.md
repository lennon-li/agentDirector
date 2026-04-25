# Agent-Director Workflow Template v3

Drop this into the root of any project where you use Claude Code, Codex, Gemini, and Copilot/GitHub agents together.

Start with:

1. Fill in `agent/PROJECT_BRIEF.md`, `agent/CURRENT_STATE.md`, and `AGENTS.md#project-context`
2. Run `prompts/00_bootstrap_check.md` — do not proceed until it reports READY
3. Read `DIRECTOR.md` and `AGENTS.md`
4. Run `prompts/01_claude_project_familiarization.md`

Core idea:

- Director owns purpose, scope, and approval.
- Claude plans.
- Codex implements one small task.
- Gemini audits.
- Project memory is updated.
- Repeat.

Prime directive:

> Agents should reduce unfinished work, not create more interesting unfinished work.


## Manager Agent Layer

This v4 version adds:

- `MANAGER.md`
- `agent/NEXT_ACTION.md`
- `prompts/00_manager_next_action.md`
- `prompts/01_manager_after_agent_handoff.md`
- `prompts/02_manager_route_current_status.md`
- `prompts/03_manager_save_audit_and_route.md`
- `prompts/04_manager_check_before_continue.md`
- `checklists/manager_routing_checklist.md`

Use this when you do not want to manually decide who goes next.

Ask the Manager Agent:

```text
Read MANAGER.md and project memory. What is next?
```

The Manager Agent should update `agent/NEXT_ACTION.md` with:
- current workflow state
- recommended next agent
- director review required
- director approval required
- exact next instruction


## Director / Manager / Agent Interaction

See:

`docs/director_manager_agent_interaction.md`

This document explains, with Mermaid graphs, how the Director, Manager, and specialized agents interact.

The key model is:

```text
Director owns purpose and approval.
Manager owns routing and next-action clarity.
Agents own specialized work.
Project memory preserves state.
```


## Human-in-the-Loop Enforcement

Every approval gate is explicit and mandatory. The following rules are enforced across all prompts and routing logic:

- Director approval must be recorded in `agent/DECISION_LOG.md` before any implementation or revision task starts.
- Codex and revision prompts (`prompts/04_codex_implement_one_task.md`, `prompts/06_revision_after_audit.md`) check for a recorded Director decision and stop if none is found.
- When an audit recommends approve, the Manager routes to Director — never directly to the next implementation task.
- The Manager stop rules include: no Director approval recorded before implementation, tests/checks failing for unclear reasons.

See `AGENTS.md §10` and `MANAGER.md §5` for the full stop-rule lists.


## Python Orchestrator (planned)

`docs/orchestrator_plan.md` contains the full implementation spec for a Python orchestrator that automates the Manager loop while keeping the Director approval gate as a hard blocking `input()`.

```text
python -m orchestrator.director_loop          # full loop
python -m orchestrator.director_loop --dry-run --once   # test Manager call only
```

The orchestrator:
1. Reads all `agent/` memory files
2. Calls Claude API as the Manager (writes `NEXT_ACTION.md` via tool use)
3. Presents the decision to the Director in the terminal
4. **Blocks on human approval** when `Director Approval Required: Yes`
5. Dispatches to the appropriate agent (Codex, Gemini, Claude, Copilot CLI) via subprocess
6. Writes the agent output to `HANDOFF_LOG.md` and loops

Implementation: see `docs/orchestrator_plan.md`. To be implemented by Codex.


## File Structure

```
agentDirector/
├── AGENTS.md                        # shared rules for all agents
├── CLAUDE.md                        # Claude Code role + rules
├── GEMINI.md                        # Gemini role + rules
├── MANAGER.md                       # Manager Agent instructions
├── DIRECTOR.md                      # Director (human) workflow guide
├── agent/
│   ├── PROJECT_BRIEF.md             # project goal and constraints
│   ├── CURRENT_STATE.md             # live workflow state
│   ├── NEXT_ACTION.md               # Manager's latest recommendation
│   ├── TASK_LEDGER.md               # task status tracker
│   ├── HANDOFF_LOG.md               # agent handoff history
│   ├── DECISION_LOG.md              # director decisions
│   ├── RISK_REGISTER.md             # open risks
│   ├── ASSUMPTIONS.md               # recorded assumptions
│   ├── VERIFICATION_LOG.md          # verification evidence
│   ├── LESSONS_LEARNED.md           # reusable lessons
│   └── STOP_RULES.md                # agent stop conditions
├── prompts/                         # copy-ready prompts for each agent
├── checklists/                      # director review checklists
├── docs/
│   ├── director_manager_agent_interaction.md
│   └── orchestrator_plan.md         # Python orchestrator implementation spec
├── orchestrator/                    # Python orchestrator (to be implemented)
└── .codex/instructions.md           # Codex role + rules
```
