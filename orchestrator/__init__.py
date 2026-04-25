from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
AGENT_DIR = REPO_ROOT / "agent"
PROMPTS_DIR = REPO_ROOT / "prompts"


def load_environment() -> None:
    load_dotenv(PACKAGE_DIR / ".env", override=False)
    load_dotenv(REPO_ROOT / ".env", override=False)


def get_env(name: str, default: str | None = None) -> str | None:
    load_environment()
    return os.environ.get(name, default)


def get_required_env(name: str) -> str:
    value = get_env(name)
    if value:
        return value
    raise RuntimeError(f"Missing required environment variable: {name}")
