# Director–Manager–Agent Interaction Model

This document explains how the **Director**, **Manager**, and **Agents** interact in this project workflow.

The goal is not full automation. The goal is **director-in-the-loop orchestration**:

> Agents do the work.  
> The Manager coordinates the workflow.  
> The Director owns judgment, purpose, approval, and stopping power.

---

# 1. Roles

## Director

The Director is the human project owner.

The Director owns:

- project purpose
- deliverable
- scope
- final approval
- deployment decisions
- stop / continue decisions
- judgment when agents disagree
- ethics, risk, and real-world meaning

The Director does **not** need to manually remember every detail. The system should surface the next decision clearly.

## Manager

The Manager is the routing and coordination layer.

The Manager reads project memory and decides:

- what state the project is in
- which agent should act next
- whether director approval is required
- what files the Director should review
- what prompt/instruction should be given next
- whether the workflow should stop

The Manager does **not** implement code or approve its own recommendation.

## Agents

Agents are specialized workers.

| Agent | Main Responsibility |
|---|---|
| Claude Code | planning, architecture, Spec Kit, design review |
| Codex | implementation, small patches, tests, bug fixes |
| Gemini | broad-context audit, hidden assumptions, integration risk |
| Copilot / GitHub Agent | PR summaries, issue triage, repo automation |

---

# 2. High-Level Interaction Graph

```mermaid
flowchart TD
    D[Director<br/>Owns purpose, scope, approval] --> M[Manager<br/>Reads memory and routes work]
    M --> PM[(Project Memory)]
    PM --> M

    M --> C[Claude Code<br/>Planner / Architect]
    M --> X[Codex<br/>Implementer]
    M --> G[Gemini<br/>Auditor]
    M --> P[Copilot / GitHub Agent<br/>Repo Assistant]

    C --> PM
    X --> PM
    G --> PM
    P --> PM

    C --> M
    X --> M
    G --> M
    P --> M

    M --> NA[agent/NEXT_ACTION.md]
    NA --> D

    D -->|Approve / Revise / Reject / Stop| M
```

---

# 3. Project Memory Graph

```mermaid
flowchart LR
    M[Manager] --> CS[CURRENT_STATE.md]
    M --> TL[TASK_LEDGER.md]
    M --> HL[HANDOFF_LOG.md]
    M --> DL[DECISION_LOG.md]
    M --> RR[RISK_REGISTER.md]
    M --> AS[ASSUMPTIONS.md]
    M --> VL[VERIFICATION_LOG.md]
    M --> LL[LESSONS_LEARNED.md]
    M --> NA[NEXT_ACTION.md]

    CS --> M
    TL --> M
    HL --> M
    DL --> M
    RR --> M
    AS --> M
    VL --> M
    LL --> M
    NA --> M
```

The Manager should never rely only on chat history. The repo files are the durable project memory.

---

# 4. Normal Feature Workflow

```mermaid
flowchart TD
    A[Director describes new feature] --> B[Manager reads memory]
    B --> C{Project / feature clear?}

    C -- No --> D[Claude clarifies project or feature]
    D --> E[Update project memory]
    E --> B

    C -- Yes --> F{Feature non-trivial?}
    F -- Yes --> G[Claude + Spec Kit create spec / plan / tasks]
    F -- No --> H[Manager prepares small implementation task]

    G --> I[Director reviews spec / plan / tasks]
    I --> J{Director approves?}

    J -- No --> K[Claude revises spec / plan / tasks]
    K --> I

    J -- Yes --> L[Codex implements one task]
    H --> L

    L --> M[Gemini audits task]
    M --> N{Audit result}

    N -- Approve --> O[Director approves task]
    N -- Revise --> P[Manager routes revision]
    N -- Reject --> Q[Director decides stop or re-plan]

    P --> R{Problem type}
    R -- Concrete code issue --> S[Codex revises same task]
    R -- Design / scope issue --> T[Claude re-plans]

    S --> M
    T --> I

    O --> U[Manager updates memory]
    U --> V{More tasks?}

    V -- Yes --> L
    V -- No --> W[Claude final review]
    W --> X[Gemini final audit]
    X --> Y[Director merge / deploy decision]
```

---

# 5. Manager Routing Logic

```mermaid
flowchart TD
    A[Manager reads project memory] --> B{Current state?}

    B -- Project unclear --> C[Route to Claude]
    B -- Feature unclear --> D[Route to Claude]
    B -- Spec missing for non-trivial feature --> E[Route to Claude + Spec Kit]
    B -- Spec created but not reviewed --> F[Route to Director]
    B -- One task ready, no Director confirmation --> K[Route to Director]
    B -- One task ready, Director confirmed --> G[Route to Codex]
    B -- Code changed, no audit --> H[Route to Gemini]
    B -- Audit says revise code --> I[Route to Codex]
    B -- Audit says design/scope problem --> J[Route to Claude]
    B -- Human approval needed --> K[Route to Director]
    B -- Memory stale --> L[Route to Manager / Claude memory update]
    B -- Final review needed --> M[Route to Claude then Gemini]
    B -- Deployment/security/schema/cost issue --> N[Route to Director]
    B -- Repeated failures or unsafe state --> O[Recommend STOP]

    C --> P[NEXT_ACTION.md]
    D --> P
    E --> P
    F --> P
    G --> P
    H --> P
    I --> P
    J --> P
    K --> P
    L --> P
    M --> P
    N --> P
    O --> P
```

---

# 6. Task-Level Loop

```mermaid
sequenceDiagram
    participant D as Director
    participant M as Manager
    participant X as Codex
    participant G as Gemini
    participant PM as Project Memory

    D->>M: What is next?
    M->>PM: Read current state, task ledger, handoffs, audits
    M->>D: Recommend Codex for Task T003 only
    D->>M: Approve routing
    M->>X: Provide task instruction
    X->>PM: Write handoff and verification evidence
    X->>M: Task complete
    M->>G: Request independent audit
    G->>PM: Save audit report
    G->>M: Approve / revise / reject
    M->>D: Summarize decision needed
    D->>PM: Approve / revise / reject / stop
```

---

# 7. Approval Gates

The Director must approve before:

```mermaid
flowchart TD
    A[Potential action] --> B{Requires Director approval?}

    B -- Scope change --> YES[Director approval required]
    B -- Deployment --> YES
    B -- Secrets / credentials --> YES
    B -- Cloud permissions --> YES
    B -- Database/schema --> YES
    B -- Billing/cost increase --> YES
    B -- Production user data --> YES
    B -- Major dependency --> YES
    B -- Large refactor --> YES
    B -- Merge to main --> YES

    B -- Small implementation task --> GATE[Director must confirm task before Manager routes to Codex]
    B -- Audit only --> NO2[Manager may route to Gemini]
    B -- Planning only --> NO3[Manager may route to Claude]
```

---

# 8. What the Manager Produces

The Manager should update:

```text
agent/NEXT_ACTION.md
```

That file should answer:

```text
What happened?
What is the current workflow state?
Who should act next?
What should they do?
What should the Director review?
Is Director approval required?
What is the exact next instruction?
Should we stop?
```

The Director should be able to open `agent/NEXT_ACTION.md` and immediately know what to do.

---

# 9. Responsibility Boundaries

```mermaid
flowchart LR
    D[Director] -->|Owns| Purpose[Purpose / Meaning / Scope / Approval]
    M[Manager] -->|Owns| Routing[Routing / State / Next Action / Memory Consistency]
    C[Claude] -->|Owns| Planning[Architecture / Planning / Spec / Review]
    X[Codex] -->|Owns| Patch[Implementation / Tests / Bug Fixes]
    G[Gemini] -->|Owns| Audit[Whole-Repo Audit / Hidden Risks]
    P[Copilot] -->|Owns| GitHub[PR / Issue / Repo Tasks]

    Purpose --> M
    Routing --> D
    Planning --> M
    Patch --> M
    Audit --> M
    GitHub --> M
```

---

# 10. Practical Daily Use

The Director only needs to ask the Manager:

```text
Read MANAGER.md and project memory. What is next?
```

The Manager should respond with:

```text
Current workflow state: NEEDS_REVISION
Recommended next agent: Codex
Human approval required: Yes
Files to review: AUDIT_T003..., data.R diff, TASK_LEDGER.md
Next instruction: [copy-ready prompt]
```

Then the Director decides:

```text
Approve / revise / reject / stop
```

This keeps the workflow human-centered without making the human manually route every step.
