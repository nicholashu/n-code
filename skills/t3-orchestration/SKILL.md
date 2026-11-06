---
name: t3-orchestration
description: Use t3-orchestration only when the user explicitly requests it for the current task. Coordinates T3 child agents, provider selection, capacity, recovery and integration review.
---

# T3 Code orchestration

Use only when the user explicitly requests t3-orchestration for this task. Discussing or editing it, or requesting children alone, does not activate it.

## Set up

- Complete routine work directly. Split larger work into user-visible outcomes with one writer per shared file. Parallelize ready, independent work when it shortens delivery.
- Use Sol 6.1 to orchestrate and Terra for bounded worker tasks. Before dispatch, read [Choose workers](references/workers.md). Follow the current runtime's delegation and completion instructions. Optimize for quality and delivery time; do not ask for spending limits or reduce useful work to save money. Honor explicit task limits.
- Choose review depth by risk and verification gaps without a routine questionnaire. Respect the user's explicit preference and required project checks. An explicit `sol-loop` request uses that workflow instead.

## Run

- Give each worker the outcome, writable paths, relevant interfaces, acceptance evidence and blockers. Link existing evidence. Keep scope, ownership, revisions, results and release holds in the existing task record; verify ownership and revisions before resuming.
- Retain task IDs and stable background request IDs. Use completion notifications, not polling or watcher agents. Count queued, running and waiting runs until terminal with no pending children. Never cancel another task to free capacity.
- Preflight infrastructure before starting another runtime. Follow its retry limit; absent one, allow one recovery attempt for setup or browser failure. Then stop that path and continue independent work. Another child does not reset the limit. Retry only with new evidence or a materially different authorized recovery.
- Fix a confirmed shared cause across its in-scope consumers. Keep unrelated cleanup out.

## Verify and finish

- Integrate the batch, then check changed behavior and affected interfaces with relevant lint, typechecks and focused tests. Reuse evidence whose source, inputs and environment still apply. Separate isolated and composed reviews need a concrete risk or requirement.
- For browser or export proof, read [Product evidence](references/product-evidence.md) before collecting it. For selected or required independent review, follow [Independent review](references/independent-review.md).
- Record the result and continue authorized, unblocked work. Stop for a real blocker, required approval, explicit limit or user pause. Release owned test resources when no dependency needs them. Create separate handoffs or waiting tasks only for a distinct ownership need.
- Finish authorized publication after required checks and review. Review grants no merge or production authority and does not override release holds.

**Reply:** completed outcomes, evidence, blockers, repeated work and publication state. Separate verified behavior from external acceptance. Report usage only when measured; never invent progress or savings.
