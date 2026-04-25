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
