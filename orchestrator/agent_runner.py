from __future__ import annotations

import subprocess
from pathlib import Path

from anthropic import Anthropic

from orchestrator import REPO_ROOT, get_env, get_required_env

COMMAND_TIMEOUT_SECONDS = 300


def _read_repo_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _run_subprocess(
    command: list[str],
    instruction: str | None = None,
    missing_message: str | None = None,
) -> str:
    try:
        result = subprocess.run(
            command,
            input=instruction,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
    except FileNotFoundError:
        return missing_message or f"ERROR: command not found at {command[0]}"
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        return (
            f"ERROR: command timed out after {COMMAND_TIMEOUT_SECONDS} seconds\n"
            f"{stdout}{stderr}"
        )
    return (result.stdout or "") + (result.stderr or "")


def _collect_text(response) -> str:
    return "\n".join(
        block.text for block in response.content if getattr(block, "type", "") == "text"
    ).strip()


def run_codex(instruction: str) -> str:
    codex_cli_path = get_env("CODEX_CLI_PATH", "codex")
    return _run_subprocess(
        [codex_cli_path, "--quiet"],
        instruction=instruction,
        missing_message=f"ERROR: codex CLI not found at {codex_cli_path}",
    )


def run_gemini(instruction: str) -> str:
    gemini_cli_path = get_env("GEMINI_CLI_PATH", "gemini")
    return _run_subprocess(
        [gemini_cli_path, "-p", instruction],
        missing_message=f"ERROR: gemini CLI not found at {gemini_cli_path}",
    )


def run_claude_architect(instruction: str) -> str:
    client = Anthropic(api_key=get_required_env("ANTHROPIC_API_KEY"))
    model = get_env("CLAUDE_ARCHITECT_MODEL", "claude-opus-4-7")
    system_prompt = (
        "--- AGENTS.md ---\n"
        f"{_read_repo_file(REPO_ROOT / 'AGENTS.md')}\n\n"
        "--- CLAUDE.md ---\n"
        f"{_read_repo_file(REPO_ROOT / 'CLAUDE.md')}"
    )
    response = client.messages.create(
        model=model,
        max_tokens=8192,
        system=system_prompt,
        messages=[{"role": "user", "content": instruction}],
    )
    return _collect_text(response)


def run_copilot_cli(instruction: str) -> str:
    return _run_subprocess(
        ["gh", "copilot", "suggest", "-t", "shell", instruction],
        missing_message="ERROR: gh CLI not found at gh",
    )


def dispatch(next_agent: str, instruction: str) -> str:
    normalized = next_agent.strip().lower()
    if normalized == "codex":
        return run_codex(instruction)
    if normalized == "gemini":
        return run_gemini(instruction)
    if normalized == "claude":
        return run_claude_architect(instruction)
    if normalized in {"copilot", "copilot cli"}:
        return run_copilot_cli(instruction)
    if normalized in {"human", "director", "stop"}:
        return ""
    print(f"[Warning] Unknown next agent: {next_agent}")
    return ""
