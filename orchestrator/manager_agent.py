from __future__ import annotations

from datetime import datetime
from pathlib import Path

from anthropic import Anthropic

from orchestrator import REPO_ROOT, get_env, get_required_env
from orchestrator import memory as memory_module

MANAGER_MEMORY_ORDER = [
    "PROJECT_BRIEF.md",
    "CURRENT_STATE.md",
    "TASK_LEDGER.md",
    "HANDOFF_LOG.md",
    "DECISION_LOG.md",
    "RISK_REGISTER.md",
    "ASSUMPTIONS.md",
    "VERIFICATION_LOG.md",
    "STOP_RULES.md",
    "NEXT_ACTION.md",
]

TOOLS = [
    {
        "name": "write_next_action",
        "description": "Write the updated NEXT_ACTION.md file",
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Full markdown content for NEXT_ACTION.md",
                }
            },
            "required": ["content"],
        },
    },
    {
        "name": "update_current_state",
        "description": "Update CURRENT_STATE.md if it is stale",
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Full markdown content for CURRENT_STATE.md",
                }
            },
            "required": ["content"],
        },
    },
]


def _read_repo_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _build_system_prompt() -> str:
    agents_md = _read_repo_file(REPO_ROOT / "AGENTS.md")
    manager_md = _read_repo_file(REPO_ROOT / "MANAGER.md")
    today = datetime.now().date().isoformat()
    return (
        "You are the Manager Agent for this project. Your role, routing rules, "
        "and stop conditions are defined in MANAGER.md.\n\n"
        f"Today's date: {today}\n\n"
        "--- AGENTS.md ---\n"
        f"{agents_md}\n\n"
        "--- MANAGER.md ---\n"
        f"{manager_md}"
    )


def _build_user_message(memory: dict[str, str]) -> str:
    sections: list[str] = ["Here is the current project memory:\n"]
    for filename in MANAGER_MEMORY_ORDER:
        title = f"{filename} (current)" if filename == "NEXT_ACTION.md" else filename
        sections.append(f"--- {title} ---\n{memory.get(filename, '(file not found)')}\n")
    sections.append(
        "Your task:\n"
        "1. Determine current workflow state.\n"
        "2. Identify next recommended agent and action.\n"
        "3. Check stop conditions.\n"
        "4. Write the updated NEXT_ACTION.md using the write_next_action tool.\n"
        "5. If CURRENT_STATE.md is stale, update it using the update_current_state tool.\n\n"
        "Use the exact NEXT_ACTION.md format from MANAGER.md §7."
    )
    return "\n".join(sections)


def run_manager(memory: dict[str, str]) -> None:
    client = Anthropic(api_key=get_required_env("ANTHROPIC_API_KEY"))
    model = get_env("CLAUDE_MANAGER_MODEL", "claude-opus-4-7")
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=_build_system_prompt(),
        messages=[{"role": "user", "content": _build_user_message(memory)}],
        tools=TOOLS,
        tool_choice={"type": "any"},
    )

    used_tools: set[str] = set()
    for block in response.content:
        if getattr(block, "type", "") != "tool_use":
            continue

        tool_input = getattr(block, "input", {}) or {}
        content = tool_input.get("content", "")
        if block.name == "write_next_action":
            memory_module.write_next_action(content)
            used_tools.add(block.name)
        elif block.name == "update_current_state":
            memory_module.update_current_state(content)
            used_tools.add(block.name)

    if "write_next_action" not in used_tools:
        raise RuntimeError("Manager response did not write NEXT_ACTION.md.")
