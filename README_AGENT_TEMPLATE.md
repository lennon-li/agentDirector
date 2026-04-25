# Agent Team Starter Template v2

This template gives each project a shared agent handbook plus lightweight project memory.

## How to use

1. Copy all files into the root of your project repo.
2. Fill in:
   - `agent/PROJECT_BRIEF.md`
   - `agent/CURRENT_STATE.md`
   - `agent/STOP_RULES.md`
   - `AGENTS.md#project-context`
3. Start with Claude Code for project familiarization and planning.
4. Use Codex for one small implementation task at a time.
5. Use Gemini for broad audit/review.
6. Use Copilot/GitHub Agent for repo-native summaries and maintenance.

## First prompt for Claude Code

Read `AGENTS.md`, `CLAUDE.md`, `agent/PROJECT_BRIEF.md`, `agent/CURRENT_STATE.md`, and `agent/STOP_RULES.md`.

This is an existing project. Before planning or coding, familiarize yourself with the project.

Inspect the repo and summarize:
1. What the project currently does
2. The main architecture/components
3. How to run it locally
4. How to test it
5. The most important files/directories
6. Any obvious risks or unclear areas

Then update:
- `agent/PROJECT_BRIEF.md`
- `agent/CURRENT_STATE.md`
- `AGENTS.md#project-context`

Do not modify application code.
Do not implement anything.
Do not expand scope.

End with the required handoff format from `AGENTS.md`.
