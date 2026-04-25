from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from orchestrator import AGENT_DIR

MEMORY_FILES = [
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
    "LESSONS_LEARNED.md",
]

SECTION_PATTERN = re.compile(r"^## (?P<header>.+?)\n(?P<body>.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
INSTRUCTION_PATTERN = re.compile(r"```text\s*(.*?)```", re.DOTALL)
DECISION_ID_PATTERN = re.compile(r"^## DECISION-", re.MULTILINE)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse_sections(content: str) -> dict[str, str]:
    return {
        match.group("header").strip(): match.group("body").strip()
        for match in SECTION_PATTERN.finditer(content)
    }


def _parse_list(section: str) -> list[str]:
    items: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def load_all_memory() -> dict[str, str]:
    memory: dict[str, str] = {}
    for filename in MEMORY_FILES:
        path = AGENT_DIR / filename
        memory[filename] = _read_text(path) if path.exists() else "(file not found)"
    return memory


def read_next_action() -> dict[str, object]:
    path = AGENT_DIR / "NEXT_ACTION.md"
    content = _read_text(path) if path.exists() else ""
    sections = _parse_sections(content)
    instruction_source = sections.get("Copy-Ready Instruction For Next Agent", "")
    instruction_match = INSTRUCTION_PATTERN.search(instruction_source)

    approval_value = sections.get("Director Approval Required?", "").strip().lower()

    return {
        "state": sections.get("Current Workflow State", "").strip(),
        "summary": sections.get("Summary", "").strip(),
        "next_agent": sections.get("Recommended Next Agent", "").strip(),
        "next_action": sections.get("Recommended Next Action", "").strip(),
        "review_files": _parse_list(sections.get("Director Must Review Before Continuing", "")),
        "approval_required": approval_value == "yes",
        "why": sections.get("Why This Is Next", "").strip(),
        "instruction": instruction_match.group(1).strip() if instruction_match else "",
        "stop_flags": _parse_list(sections.get("Stop / Caution Flags", "")),
    }


def write_next_action(content: str) -> None:
    (AGENT_DIR / "NEXT_ACTION.md").write_text(content, encoding="utf-8")


def update_current_state(content: str) -> None:
    (AGENT_DIR / "CURRENT_STATE.md").write_text(content, encoding="utf-8")


def append_handoff(agent_name: str, task: str, output: str) -> None:
    path = AGENT_DIR / "HANDOFF_LOG.md"
    timestamp = datetime.now().date().isoformat()
    entry = (
        f"### {timestamp}\n"
        f"**Agent:** {agent_name}\n"
        f"**Task:** {task}\n"
        f"**Output:**\n"
        f"{output}\n"
        "---\n"
    )
    prefix = ""
    if path.exists():
        existing = _read_text(path)
        prefix = "" if existing.endswith("\n") or not existing else "\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(prefix + entry)


def write_decision(
    task_id: str,
    decision: str,
    reason: str,
    next_action: str,
    next_agent: str,
) -> None:
    path = AGENT_DIR / "DECISION_LOG.md"
    existing = _read_text(path) if path.exists() else ""
    decision_id = len(DECISION_ID_PATTERN.findall(existing)) + 1
    entry = (
        f"## DECISION-{decision_id:03d}\n\n"
        f"### Date\n"
        f"{datetime.now().date().isoformat()}\n\n"
        f"### Task ID\n"
        f"{task_id}\n\n"
        f"### Decision\n"
        f"{decision}\n\n"
        f"### Reason\n"
        f"{reason}\n\n"
        f"### Director\n"
        f"Human\n\n"
        f"### Next Action\n"
        f"{next_action}\n\n"
        f"### Next Agent\n"
        f"{next_agent}\n"
    )
    separator = ""
    if existing and not existing.endswith("\n\n"):
        separator = "\n\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(separator + entry)
