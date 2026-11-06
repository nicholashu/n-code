---
name: t3-orchestration
description: Coordinates substantial work in T3 Code through child agents, provider selection, capacity limits, rate-limit recovery and integration review. Use when the user explicitly requests T3 orchestration.
---

## T3 Code orchestration

Use this skill when the user explicitly requests T3 orchestration. Editing, reviewing or discussing this skill does not activate orchestration or authorize dispatch. Follow the current runtime's instructions and the user's delegation, provider and model boundaries. Resolve providers and models against the live catalog before dispatch; use only authorized, available settings. Respect provider and host capacity limits. Never substitute a provider or model without authorization.

### Keep work proportional

- Complete routine changes directly. Use authorized capacity to advance independent, ready work in parallel. Choose concurrency to shorten delivery time within the budget, accounting for briefing, coordination and integration. Reduce concurrency when contention or integration overhead outweighs the benefit; do not leave useful independent work idle merely to minimize agent count.
- Define a small batch by a user-visible outcome and its shared interfaces. Parallelize disjoint work and keep one owner for shared files. Integrate the batch before its full verification and review. Separate isolated and composed review journeys need a specific risk or an explicit requirement; do not make both routine.
- Choose the smallest check that answers the remaining question. Reuse passing evidence when the relevant source, inputs and environment remain applicable; verify changed behavior and affected interfaces. Do not rerun unchanged suites or historical audits merely because a new agent took over.
- When a defect comes from a shared control, renderer or workflow, inspect its other in-scope consumers before continuing one type at a time. Fix the confirmed shared cause together and check affected behavior; do not turn that inspection into unrelated cleanup or a full-suite campaign.
- Diagnose infrastructure failures with the cheapest preflight before allocating another full runtime. Follow the runtime's recovery limit; if none is given for a setup or browser failure, allow one bounded recovery attempt after the initial failure. Then stop that blocked path and continue independent work. A new child or UUID does not reset the same failure; require new evidence or a materially different authorized recovery before retrying.
- Keep briefs to the outcome, write ownership, relevant interfaces, acceptance checks and known blockers. Link existing evidence instead of copying its history. Maintain one current task record with short result summaries; create extra handoff documents only for a real ownership need.
- Track completed user-visible outcomes, tooling blockers and work repeated per batch. Use available elapsed-time and token measurements without creating a separate reporting system; test totals and review rounds are not delivery measures. Respect stated budgets and disclose missing usage data rather than inventing savings, completion percentages or unsupported date ranges.

### Make product evidence reusable

Apply this section when the task requires browser or exported-output proof. Reuse a project-owned collector or existing harness; do not build a new framework for each slice.

1. **Preflight the collector.** Check fixture/schema compatibility, required bootstrap configuration and runtime readiness before the full journey. Verify the intended route/resource, saved revision and selected controls before mutation. Wait for loaded fonts, expected saved values and a settled export state before measuring or claiming refusal. Use the authorized browser; this section grants no alternate-browser access.
2. **Retain evidence at the event.** Copy every required download into the owned evidence directory immediately, verify its identity and bind it to the resource/revision and audience before closing the tab or cleaning up. Keep initial captures before the first mutation when that ordering is needed to prove the claim. Prefer one concise record of these associations over per-step prose receipts.
3. **Check representative layouts early.** Inspect one real example of each distinct renderer, audience layout or export path before processing a whole collection. Reuse the proven capture method, but inspect required final outputs; one representative does not prove every layout.
4. **Classify a failed step.** Distinguish a product defect, an infrastructure/collector failure and a missing-evidence limitation. State the claim left unproved. A missing screenshot or receipt alone does not demonstrate a product defect; it can still leave an explicit required gate open.
5. **Supplement the missing claim.** Use a targeted capture when source, inputs and relevant state can be established. Replay only the steps needed to resolve a consequential uncertainty; repeat the full journey when that state or causal sequence cannot otherwise be established. Preserve historical failures and verdicts, label retrospective counts and separate timelines, and never backdate evidence or silently weaken required acceptance.

### Choose providers

Before dispatch, if the user has not already specified the providers for this task, ask which agent pool to use with the runtime's multiple-choice question tool when available:

1. Ollama Cloud, OpenCode Free and OpenAI (Codex).
2. OpenCode Free only.
3. Ollama Cloud only.
4. OpenAI (Codex) only.

Offer a free-text response when supported, so the user can choose another combination or specify models. If no question tool is available, ask in conversation. Wait for the answer before dispatch; a preselected or unanswered option is not consent. If the user has already supplied a provider choice, use it without asking again. Apply the selected pool to review and rate-limit recovery as well, and follow the current runtime's model-selection and delegation rules. Report unavailable choices rather than silently switching providers.

### Review and spending choices

When the choice of independent review would materially affect the work and the user has not already specified a review level, ask with the runtime's multiple-choice question tool when available:

1. Use your judgment — choose review based on risk and complexity.
2. Thorough review — use the independent review loop below.
3. No independent review — verify directly.

If no question tool is available, ask in conversation. Wait for the answer before dependent review work; a preselected or unanswered option is not consent. Do not ask for a routine review decision on every task. Follow any required review imposed by higher-priority instructions or project rules; if a selection conflicts with such a requirement, explain the constraint rather than bypass it.

When expected spending could be significant and the acceptable limit cannot be inferred from the request or prior direction, ask for a spending limit before incurring dependent costs. Otherwise proceed within the user's stated budget and the active runtime's authorization rules.

### Worker pool

Resolve these configured choices against the live catalog before dispatch. Their use and any fallback remain subject to the user's request and current runtime rules.

- **Ollama Cloud:** `ollama_cloud`, model `ollama-cloud/deepseek-v4.1-flash-1017`, for bounded implementation, investigation and independent analysis. Allow at most three concurrent Ollama Cloud runs, including main-thread runs and nested children sharing the provider.
- **OpenCode Free:** `opencode_free`, using a currently available model explicitly labelled free, for bounded research, implementation and verification. Prefer the latest GLM Flash or DeepSeek Flash; respect rate limits and provider capacity.
- **Codex:** `codex`, model `gpt-6.1-sol` with `options:{reasoningEffort:"high"}` for complex implementation, integration advice and independent review; `gpt-6.1-terra` with `options:{reasoningEffort:"xhigh"}` for focused implementation, tests and smaller investigations.

Count queued, running and waiting runs against capacity until terminal, and never cancel another task to make room. Preserve all provider, host and app limits.

### Rate-limit recovery

When a delegated task encounters a rate limit, retry unfinished work using the following order only when the user and runtime authorize the provider and model. Skip unavailable, already attempted or cooling-down candidates; resolve exact IDs against the live catalog:

1. `opencode_free` / `opencode/deepseek-v4.1-flash-free`.
2. `opencode_free` / `opencode/glm-5.3-flash-free`.
3. `ollama_cloud` / `ollama-cloud/deepseek-v4.1-flash:1017`.
4. `codex` / `gpt-6.1-terra`, with `options:{reasoningEffort:"xhigh"}`.

The Ollama pool and fallback IDs above differ as in the source configuration; verify the live catalog instead of assuming either ID is available. If switching is not authorized, report the limit instead of silently substituting a model.

Follow each delegated task's supported completion mechanism. Keep task identifiers and cancel only work within the authorized scope. Do not poll or create watcher agents when the runtime provides notifications. Report unavailable providers and failed or incomplete work accurately.

- The main orchestrator decides whether independent review is warranted by task risk, complexity, impact and gaps in verification. Security, authentication, billing, data integrity, concurrency, broad changes and uncertain behavior are signals for stronger review; small, low-risk changes may finish with direct verification. Respect the selected review level and required project checks; when using judgment and review adds value, use the independent review loop below. If another explicitly requested review workflow applies, follow its rules instead of duplicating it.
- After integrating changes, verify the composed result with the relevant typechecks, lint and focused tests. Present the verified result and outstanding limits back to the human.

## Task completion and outside dependencies

Use the existing task record for scope, owners, dependencies, source revision, outcome, evidence, blockers, next action and release holds. The parent owns the shared record; children own only assigned handoffs. Before resuming, read the record and verify current ownership and revisions; recheck affected work when inputs changed. Keep secrets out. Create a separate waiting task only when a distinct owner or lifecycle needs one. Distinguish delivered work from external acceptance; do not claim a response or cleanup that has not occurred. Release owned test resources promptly unless a real dependency requires them to remain. Use supported completion notifications rather than polling.

A checkpoint preserves continuity; it is not a routine stop. After recording a completed batch, continue the next unblocked, already-authorized slice without waiting for another "continue". Stop dependent work for a real blocker, required approval or user pause, and respect runtime handoff and budget limits. Do not infer authorization for new scope, publication or release.

For visual work, keep a compact, current example index or gallery when it helps the user assess progress. Distinguish implemented source, verified local behavior/output and outstanding external acceptance. Add evidence links as batches finish instead of reconstructing a catalogue at the end; do not create an extra artifact when the existing task record is sufficient.

## Independent review loop

Respect the selected review level and required project checks. Efficiency does not waive security, data integrity, concurrency, actual-output or release requirements.

1. **Identify the candidate.** Record the base/candidate revision, scoped changes including untracked files, acceptance checks and known failures. A scoped Git diff and test results normally suffice. Whole-checkout copies, hash sweeps and historical bundle audits need an explicit requirement or a concrete integrity risk. Keep the candidate stable during its review.
2. **Review the composed change once.** Use one authorized reviewer through the runtime's supported delegation method. Provide the relevant diff, connected interfaces, available check results and evidence links. Require concrete findings, severity, reproduction, smallest fix and an APPROVE/CHANGES verdict; no nested reviewers. Read the project's writing-tests guidance before testing work. The reviewer reruns only checks needed to assess an unresolved risk or verify a material claim, identifying inherited results accurately.
3. **Resolve findings directly.** Verify each finding and make the smallest justified in-scope repair. Record fixed, disputed or declined findings in the existing task record and run affected checks. Avoid a new implementation child for a small repair. Preserve scope, permissions and unrelated work.
4. **Recheck the delta when needed.** One review is normally enough; use a targeted follow-up for material repairs or unresolved findings. Give it the changed behavior, prior findings and relevant evidence instead of restarting the entire review. Cosmetic changes and declined nits do not require another round. After two passes without material progress, reassess the cause, scope and budget before further delegation; another pass needs a concrete unresolved risk and expected new evidence. Follow any explicitly required review workflow.
5. **Close on sufficient evidence.** Resolve required findings and complete relevant checks. Optional nits alone need not keep a task open; record the parent's disposition without inventing reviewer approval. A timeout, exhausted budget or unavailable reviewer cannot satisfy a required review. Report the precise remaining blocker and continue independent authorized work.
6. **Hand off or publish within authority.** Once applicable review closes, finish already-authorized commit, push or draft-PR work. Review grants no merge or production authority and does not override project holds. Report the resulting behavior, material checks, remaining limits and publication state concisely.
