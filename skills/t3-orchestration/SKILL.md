---
name: t3-orchestration
description: Coordinate T3 child agents for substantial tasks with independent work or a need for specialist review. Use when requested. Handle small or tightly coupled tasks directly.
---

# T3 Code orchestration

Use when the user explicitly requests T3 orchestration, or when independent work or specialist review would help a substantial task. The current runtime must permit delegation. Work directly for simple, small, tightly coupled or sequential tasks, and when coordination would add more overhead than value. Discussing or editing this skill alone does not activate it. Honor explicit limits on delegation and current runtime rules.

## Set up

- Complete routine work directly. Split larger tasks by outcome, with one writer per shared file. Run independent work in parallel when it saves time.
- Keep coordination in the current thread with its current model. Scope the work, dispatch workers, integrate results and assess evidence. Do not spawn an orchestrator child or switch models to satisfy this skill. Use Terra for bounded worker tasks. Before dispatch, read [Choose workers](references/workers.md). Follow the current runtime's delegation and completion instructions. Prioritize quality and delivery time. Do not ask for spending limits or cut useful work to save money. Honor explicit task limits.
- Choose review depth based on risk and missing evidence. Do not ask routine setup questions. Respect the user's explicit preference and required project checks. An explicit `sol-loop` request uses that workflow instead.

## Run

- Tell each worker the required outcome, paths it may edit, affected interfaces, evidence it must provide and known blockers. Link existing evidence. Keep scope, ownership, revisions, results and release holds in the existing task record; verify ownership and revisions before resuming.
- Retain task IDs and stable background request IDs. Use completion notifications, not polling or watcher agents. Count queued, running and waiting runs against capacity until they finish and have no pending children. Never cancel another task to free capacity.
- Check infrastructure before starting another runtime. Follow its retry limit; absent one, allow one recovery attempt for setup or browser failure. Then stop that path and continue independent work. Another child does not reset the limit. Retry only with new evidence or a materially different authorized recovery.
- When a shared cause is confirmed, fix it for every affected caller within scope. Leave unrelated code alone.

## Verify and finish

- Integrate the batch, then check changed behavior and affected interfaces with relevant lint, typechecks and focused tests. Reuse evidence whose source, inputs and environment still apply. Reviewing workers separately and again after integration needs a specific risk or requirement.
- For browser or export proof, read [Product evidence](references/product-evidence.md) before collecting it. For selected or required independent review, follow [Independent review](references/independent-review.md).
- Record the result and continue authorized, unblocked work. Stop for a real blocker, required approval, explicit limit or user pause. Release owned test resources when no dependency needs them. Create a separate handoff or waiting task only when another owner needs it.
- Finish authorized publication after required checks and review. Review grants no merge or production authority and does not override release holds.

Report what finished, the evidence, blockers, repeated work and publication status. Distinguish what you verified from what external reviewers accepted. Report usage only when measured; never invent progress or savings.
