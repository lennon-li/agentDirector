from __future__ import annotations

import argparse
from datetime import datetime

from orchestrator import memory
from orchestrator.agent_runner import dispatch
from orchestrator.human_gate import confirm_agent_dispatch, present_next_action, request_approval
from orchestrator.manager_agent import run_manager


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the agentDirector orchestration loop.")
    parser.add_argument("--dry-run", action="store_true", help="Run the manager and print the next action without dispatching.")
    parser.add_argument("--once", action="store_true", help="Run a single manager cycle and exit.")
    return parser.parse_args()


def extract_current_task_id(memory_snapshot: dict[str, str]) -> str:
    task_ledger = memory_snapshot.get("TASK_LEDGER.md", "")
    for line in task_ledger.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 3:
            continue
        if cells[0] == "Task ID" or cells[0].startswith("---"):
            continue
        if cells[2] in {"IN_PROGRESS", "NEEDS_AUDIT"}:
            return cells[0]
    return "N/A"


def print_banner() -> None:
    print("╔══════════════════════════════════════════════════════╗")
    print("║  agentDirector — Director Loop                       ║")
    print("║  Human-in-the-loop AI orchestration                  ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(datetime.now().strftime("%Y-%m-%d"))


def main() -> None:
    args = parse_args()
    print_banner()

    while True:
        print("\n[Manager] Reading project memory...")
        memory_snapshot = memory.load_all_memory()

        print("[Manager] Calling Claude API...")
        run_manager(memory_snapshot)

        next_action = memory.read_next_action()
        present_next_action(next_action)

        state = str(next_action["state"])
        next_agent = str(next_action["next_agent"]).lower()
        instruction = str(next_action["instruction"])

        if state == "SHOULD_STOP" or next_agent == "stop":
            print("\n[STOP] Manager recommends stopping. Exiting.")
            break

        if args.dry_run:
            print("[dry-run] Would dispatch to:", next_agent)
            if args.once:
                break
            continue

        if bool(next_action["approval_required"]):
            decision, reason = request_approval(required=True)
            if decision == "stop":
                print("\n[STOP] Director chose to stop.")
                break

            task_id = extract_current_task_id(memory_snapshot)
            memory.write_decision(
                task_id,
                decision,
                reason,
                str(next_action["next_action"]),
                str(next_action["next_agent"]),
            )

            if decision == "reject":
                print("[Director] Decision recorded. Looping back to Manager.")
                continue

            if decision == "revise":
                print("[Director] Decision recorded. Please provide revised instruction.")
                revised = input("Revised instruction: ").strip()
                if revised:
                    instruction = revised

        if next_agent in {"human", "director"}:
            print("[Human gate] Director action required. Loop back after completing manually.")
            input("Press ENTER when done...")
        else:
            should_dispatch = True
            if next_agent == "codex":
                should_dispatch = confirm_agent_dispatch(next_agent, instruction)

            if not should_dispatch:
                print("[Skipped] Dispatch cancelled by Director.")
            else:
                print(f"\n[Agent] Running {next_agent}...")
                output = dispatch(next_agent, instruction)
                print(f"\n[Agent output]\n{output[:2000]}")
                memory.append_handoff(str(next_action["next_agent"]), str(next_action["next_action"]), output)

        if args.once:
            break


if __name__ == "__main__":
    main()
