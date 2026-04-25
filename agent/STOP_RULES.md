# Stop Rules

Agents must stop and ask the director before:

- changing project objective or deliverable
- expanding scope
- deploying
- changing secrets, credentials, auth, or cloud permissions
- changing database/schema design
- adding major dependencies
- making irreversible changes
- touching billing, production infrastructure, or user data
- continuing after two failed attempts at the same issue
- continuing when tests/checks fail for unclear reasons
- continuing when the diff exceeds 200 lines changed or 5 files touched in a single task
- continuing when requirements conflict
