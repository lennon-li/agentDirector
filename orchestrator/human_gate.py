from __future__ import annotations


def _format_list(items: list[str]) -> str:
    if not items:
        return "  (none)"
    return "\n".join(f"  {item}" for item in items)


def _preview(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return f"{text[:limit]}..."


def present_next_action(na: dict[str, object]) -> None:
    approval = "Yes" if na.get("approval_required") else "No"
    review_files = _format_list(list(na.get("review_files", [])))
    stop_flags = _format_list(list(na.get("stop_flags", [])))
    instruction = _preview(str(na.get("instruction", "")), 300)

    print("╔══════════════════════════════════════════════════════╗")
    print("║  MANAGER UPDATE                                      ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()
    print(f"State:         {na.get('state', '')}")
    print(f"Next Agent:    {na.get('next_agent', '')}")
    print(f"Approval:      {approval}")
    print()
    print("Summary:")
    print(f"  {na.get('summary', '')}")
    print()
    print("Files to review:")
    print(review_files)
    print()
    print("Stop / Caution flags:")
    print(stop_flags)
    print()
    print("Instruction for next agent:")
    print(f"  {instruction}")


def request_approval(required: bool) -> tuple[str, str]:
    if required:
        valid_decisions = {"approve", "revise", "reject", "stop"}
        while True:
            print("Decision required. Enter: approve / revise / reject / stop")
            decision = input("Decision: ").strip().lower()
            if decision in valid_decisions:
                reason = input("Reason (optional): ").strip()
                return decision, reason
            print("Invalid decision. Please enter approve, revise, reject, or stop.")

    response = input("Press ENTER to continue, or type 'stop' to halt: ").strip().lower()
    if response == "stop":
        return "stop", ""
    return "continue", ""


def confirm_agent_dispatch(next_agent: str, instruction: str) -> bool:
    preview = _preview(instruction, 200)
    print(f"About to dispatch to: {next_agent}")
    print(f"Instruction preview: {preview}")
    print()
    while True:
        response = input("Confirm dispatch? [y/n]: ").strip().lower()
        if response in {"y", "yes"}:
            return True
        if response in {"n", "no"}:
            return False
        print("Please enter y or n.")
