# Plan: Director Loop Orchestrator

## Context

The `agentDirector` project defines a human-in-the-loop workflow where a Director (human) controls a Manager (AI) that routes tasks to specialist agents (Codex, Gemini, Claude Architect, Copilot CLI). Currently the human manually:
1. Pastes prompts into agent sessions
2. Reads `agent/NEXT_ACTION.md`
3. Types an approval decision
4. Pastes the next prompt into the next agent

This plan automates steps 1, 2, and 4 with a Python orchestrator script. Step 3 (human approval) remains a hard blocking gate. The existing `agent/` memory files are the durable state machine — the orchestrator drives them.

---

## Files to Create

```
orchestrator/
├── __init__.py
├── director_loop.py      # main entry point + CLI arg parsing + loop
├── memory.py             # read/write all agent/ files
├── manager_agent.py      # call Claude API as Manager (with tool use)
├── agent_runner.py       # delegate to Codex/Gemini/Copilot/Claude subprocesses
└── human_gate.py         # blocking approval gate + write decision to DECISION_LOG.md
requirements.txt
.env.example
```

No application code is modified. All changes are additive.

---

## Config / Environment

`.env.example`:
```
ANTHROPIC_API_KEY=your_key_here
CODEX_CLI_PATH=codex
GEMINI_CLI_PATH=gemini
CLAUDE_MANAGER_MODEL=claude-opus-4-7
CLAUDE_ARCHITECT_MODEL=claude-opus-4-7
```

Load via `python-dotenv`. Fall back to `os.environ`. Fail fast with a clear error if `ANTHROPIC_API_KEY` is missing.

`REPO_ROOT` = directory two levels above `orchestrator/` (auto-detected from `__file__`).
`AGENT_DIR` = `{REPO_ROOT}/agent`
`PROMPTS_DIR` = `{REPO_ROOT}/prompts`

---

## `memory.py`

### Constants
```python
MEMORY_FILES = [
    "PROJECT_BRIEF.md", "CURRENT_STATE.md", "TASK_LEDGER.md",
    "HANDOFF_LOG.md", "DECISION_LOG.md", "RISK_REGISTER.md",
    "ASSUMPTIONS.md", "VERIFICATION_LOG.md", "STOP_RULES.md",
    "NEXT_ACTION.md", "LESSONS_LEARNED.md",
]
```

### Functions

**`load_all_memory() -> dict[str, str]`**
- Read each file in `MEMORY_FILES` from `AGENT_DIR`
- Return `{filename: content}`. Missing files return `"(file not found)"`.

**`read_next_action() -> dict`**
Parse `agent/NEXT_ACTION.md` using regex on `## ` headers. Return:
```python
{
    "state": str,           # "## Current Workflow State" value
    "summary": str,
    "next_agent": str,      # "Claude" | "Codex" | "Gemini" | "Copilot" | "Human" | "Stop"
    "next_action": str,
    "review_files": list[str],
    "approval_required": bool,  # True if value is "Yes"
    "why": str,
    "instruction": str,     # content inside ```text ... ``` block
    "stop_flags": list[str],
}
```
Parse the ` ```text ... ``` ` block for `instruction` using regex: `` r'```text\s*(.*?)```' `` with `re.DOTALL`.

**`write_next_action(content: str)`**
Overwrite `agent/NEXT_ACTION.md` with `content`. UTF-8.

**`update_current_state(content: str)`**
Overwrite `agent/CURRENT_STATE.md` with `content`. UTF-8.

**`append_handoff(agent_name: str, task: str, output: str)`**
Append a handoff entry to `agent/HANDOFF_LOG.md` using the template format:
```
### {date}
**Agent:** {agent_name}
**Task:** {task}
**Output:**
{output}
---
```

**`write_decision(task_id: str, decision: str, reason: str, next_action: str, next_agent: str)`**
- Auto-increment decision ID: count existing `## DECISION-` lines in `DECISION_LOG.md`, add 1.
- Append to `agent/DECISION_LOG.md` using `DECISION_TEMPLATE.md` format:
```markdown
## DECISION-{ID:03d}

### Date
{YYYY-MM-DD}

### Task ID
{task_id}

### Decision
{decision}

### Reason
{reason}

### Director
Human

### Next Action
{next_action}

### Next Agent
{next_agent}
```

---

## `manager_agent.py`

**`run_manager(memory: dict) -> None`**

Calls the Claude API with the Manager persona. The Manager **uses tool use** to write files — it does not return file content in the response body.

### System prompt (build dynamically):
```
You are the Manager Agent for this project. Your role, routing rules, and stop conditions are defined in MANAGER.md.

Today's date: {date}

--- AGENTS.md ---
{agents_md}

--- MANAGER.md ---
{manager_md}
```

### User message:
```
Here is the current project memory:

--- PROJECT_BRIEF.md ---
{content}

--- CURRENT_STATE.md ---
{content}

--- TASK_LEDGER.md ---
{content}

--- HANDOFF_LOG.md ---
{content}

--- DECISION_LOG.md ---
{content}

--- RISK_REGISTER.md ---
{content}

--- ASSUMPTIONS.md ---
{content}

--- VERIFICATION_LOG.md ---
{content}

--- STOP_RULES.md ---
{content}

--- NEXT_ACTION.md (current) ---
{content}

Your task:
1. Determine current workflow state.
2. Identify next recommended agent and action.
3. Check stop conditions.
4. Write the updated NEXT_ACTION.md using the write_next_action tool.
5. If CURRENT_STATE.md is stale, update it using the update_current_state tool.

Use the exact NEXT_ACTION.md format from MANAGER.md §7.
```

### Tools provided to Manager:
```python
tools = [
    {
        "name": "write_next_action",
        "description": "Write the updated NEXT_ACTION.md file",
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "Full markdown content for NEXT_ACTION.md"}
            },
            "required": ["content"]
        }
    },
    {
        "name": "update_current_state",
        "description": "Update CURRENT_STATE.md if it is stale",
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "Full markdown content for CURRENT_STATE.md"}
            },
            "required": ["content"]
        }
    }
]
```

### Tool execution:
After API call, iterate `response.content` blocks:
- `type == "tool_use"` and `name == "write_next_action"` → call `memory.write_next_action(input["content"])`
- `type == "tool_use"` and `name == "update_current_state"` → call `memory.update_current_state(input["content"])`

Use `max_tokens=4096`. Model from config `CLAUDE_MANAGER_MODEL`.

---

## `agent_runner.py`

**`run_codex(instruction: str) -> str`**
```python
result = subprocess.run(
    [CODEX_CLI_PATH, "--quiet"],
    input=instruction,
    capture_output=True, text=True, timeout=300
)
return result.stdout + result.stderr
```
On `FileNotFoundError`: return error string `"ERROR: codex CLI not found at {path}"`.

**`run_gemini(instruction: str) -> str`**
```python
result = subprocess.run(
    [GEMINI_CLI_PATH, "-p", instruction],
    capture_output=True, text=True, timeout=300
)
return result.stdout + result.stderr
```

**`run_claude_architect(instruction: str) -> str`**
Call Claude API directly (not subprocess). System prompt = contents of `CLAUDE.md` + `AGENTS.md`. User message = `instruction`. Model = `CLAUDE_ARCHITECT_MODEL`. `max_tokens=8192`. Return text content.

**`run_copilot_cli(instruction: str) -> str`**
```python
result = subprocess.run(
    ["gh", "copilot", "suggest", "-t", "shell", instruction],
    capture_output=True, text=True, timeout=300
)
return result.stdout + result.stderr
```

**`dispatch(next_agent: str, instruction: str) -> str`**
Route by `next_agent` string (case-insensitive):
- `"codex"` → `run_codex`
- `"gemini"` → `run_gemini`
- `"claude"` → `run_claude_architect`
- `"copilot"` / `"copilot cli"` → `run_copilot_cli`
- `"human"` / `"director"` / `"stop"` → return `""` (caller handles)
- Unknown → print warning, return `""`

---

## `human_gate.py`

**`present_next_action(na: dict)`**
Print a formatted summary to stdout:
```
╔══════════════════════════════════════════════════════╗
║  MANAGER UPDATE                                      ║
╚══════════════════════════════════════════════════════╝

State:         {state}
Next Agent:    {next_agent}
Approval:      {Yes/No}

Summary:
  {summary}

Files to review:
  {review_files}

Stop / Caution flags:
  {stop_flags}

Instruction for next agent:
  {instruction[:300]}...
```

**`request_approval(required: bool) -> tuple[str, str]`**
If `required`:
```
Decision required. Enter: approve / revise / reject / stop
Decision: _
Reason (optional): _
```
Block on `input()`. Validate decision is one of the four values. Loop until valid.
If not required (informational):
```
Press ENTER to continue, or type 'stop' to halt: _
```
Return `(decision, reason)`.

**`confirm_agent_dispatch(next_agent: str, instruction: str) -> bool`**
Always confirm before dispatching to a code-modifying agent (Codex):
```
About to dispatch to: {next_agent}
Instruction preview: {instruction[:200]}...

Confirm dispatch? [y/n]: _
```
Return True/False.

---

## `director_loop.py`

### CLI args
```
python -m orchestrator.director_loop [--dry-run] [--once]
```
- `--dry-run`: run Manager and show NEXT_ACTION.md, but do not dispatch to any agent or request approval
- `--once`: run one Manager cycle then exit (useful for testing)

### Main loop
```python
def main():
    print_banner()  # show project name + date

    while True:
        print("\n[Manager] Reading project memory...")
        memory = load_all_memory()

        print("[Manager] Calling Claude API...")
        run_manager(memory)  # writes NEXT_ACTION.md via tool use

        na = read_next_action()
        present_next_action(na)

        state = na["state"]
        next_agent = na["next_agent"].lower()
        approval_required = na["approval_required"]
        instruction = na["instruction"]

        # Hard stop
        if state == "SHOULD_STOP" or next_agent == "stop":
            print("\n[STOP] Manager recommends stopping. Exiting.")
            break

        # Approval gate
        if approval_required:
            decision, reason = request_approval(required=True)
            if decision == "stop":
                print("\n[STOP] Director chose to stop.")
                break
            task_id = extract_current_task_id(memory)
            write_decision(task_id, decision, reason, na["next_action"], na["next_agent"])
            if decision == "reject":
                print("[Director] Decision recorded. Looping back to Manager.")
                continue
            if decision == "revise":
                print("[Director] Decision recorded. Please provide revised instruction.")
                revised = input("Revised instruction: ").strip()
                if revised:
                    instruction = revised

        # Skip dispatch in dry-run
        if args.dry_run:
            print("[dry-run] Would dispatch to:", next_agent)
            if args.once:
                break
            continue

        # Dispatch
        if next_agent in ("human", "director"):
            print("[Human gate] Director action required. Loop back after completing manually.")
            input("Press ENTER when done...")
        else:
            if not confirm_agent_dispatch(next_agent, instruction):
                print("[Skipped] Dispatch cancelled by Director.")
            else:
                print(f"\n[Agent] Running {next_agent}...")
                output = dispatch(next_agent, instruction)
                print(f"\n[Agent output]\n{output[:2000]}")
                append_handoff(next_agent, na["next_action"], output)

        if args.once:
            break
```

**`extract_current_task_id(memory: dict) -> str`**
Find the first row in `TASK_LEDGER.md` with status `IN_PROGRESS` or `NEEDS_AUDIT`. Return task ID. Fall back to `"N/A"`.

**`print_banner()`**
```
╔══════════════════════════════════════════════════════╗
║  agentDirector — Director Loop                       ║
║  Human-in-the-loop AI orchestration                  ║
╚══════════════════════════════════════════════════════╝
```

---

## `requirements.txt`

```
anthropic>=0.40.0
python-dotenv>=1.0.0
```

---

## `.env.example`

```
ANTHROPIC_API_KEY=your_key_here
CLAUDE_MANAGER_MODEL=claude-opus-4-7
CLAUDE_ARCHITECT_MODEL=claude-opus-4-7
CODEX_CLI_PATH=codex
GEMINI_CLI_PATH=gemini
```

---

## Verification

After Codex implements:

1. `cd agentDirector && pip install -r requirements.txt`
2. Copy `.env.example` to `.env`, fill in `ANTHROPIC_API_KEY`
3. `python -m orchestrator.director_loop --dry-run --once`
   - Should call Claude API, write `agent/NEXT_ACTION.md`, print summary, exit
4. `python -m orchestrator.director_loop --once`
   - Should ask for approval (since PROJECT_BRIEF is TODO → bootstrap state)
   - Should not dispatch to any agent before human confirms
5. Verify `agent/NEXT_ACTION.md` is updated with real content after step 3
6. Verify no application code was touched

---

## Constraints for Codex

- Do not modify any existing files (AGENTS.md, prompts/, agent/, etc.)
- All new code goes under `orchestrator/`
- All file I/O uses UTF-8 encoding
- Subprocess calls must have timeouts (300s default)
- Never auto-approve — `request_approval()` must always block on human input when `required=True`
- Never dispatch to Codex without `confirm_agent_dispatch()` returning True
- Use `anthropic` SDK tool_use (not streaming) for Manager call
