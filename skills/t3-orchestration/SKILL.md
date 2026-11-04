---
name: t3-orchestration
description: Coordinates substantial work in T3 Code through child agents, provider selection, capacity limits, rate-limit recovery and integration review. Use when the user explicitly requests T3 orchestration.
---

## T3 Code orchestration

Use this skill when the user explicitly requests T3 orchestration. Follow the current runtime's instructions and the user's delegation, provider and model boundaries. Resolve providers and models against the live catalog before dispatch; use only authorized, available settings. Respect provider and host capacity limits. Never substitute a provider or model without authorization.

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

- The main orchestrator decides whether independent review is warranted by task risk, complexity, impact and gaps in verification. Security, authentication, billing, data integrity, concurrency, broad changes and uncertain behavior are signals for stronger review; small, low-risk changes may finish with direct verification. When review adds value, run the independent review loop below automatically. If another explicitly requested review workflow applies, follow its rules instead of duplicating it.
- After integrating changes, verify the composed result with the relevant typechecks, lint and focused tests. Present the verified result and outstanding limits back to the human.

## Task completion and outside dependencies

- Define each task's acceptance condition and the evidence needed to close it.
  Record the actual evidence in its task record before closing.
- When later work needs a response from another person or service, give that
  wait its own tracked task. Record who or what it awaits, the confirmation
  required, and the supported callback or next-check method. Keep it open until
  that confirmation is recorded.
- Separate delivery, receiving the response, and dependent cleanup when they
  have different completion events. Cleanup stays blocked by the response task.
  A request limited to preparing or sending work ends at its own acceptance
  condition; add outside waits only when the requested outcome depends on them.
- Use the current runtime's supported wakeup or watch mechanism for waiting.
  Preserve pending status and next steps when handing back; existing polling,
  scheduling and approval rules still apply.

## Independent review loop

1. **Freeze the scope.** Record intent, acceptance criteria, exclusions, the base
   commit and scoped paths or deliverable version. Include untracked task files;
   preserve unrelated edits. Run covering checks and disclose missing or
   pre-failing checks. Keep the same base and scope throughout the loop.
2. **Dispatch one reviewer.** Prefer an authorized `codex` / Sol reviewer when available, using the current runtime's supported delegation method. Retain the task identifier. Include the original brief,
   full scoped diff or deliverable, connected files, check results and known
   limits. Require read-only review, no nested agents, stable finding IDs,
   severity, a concrete failure case, smallest fix and an APPROVE/CHANGES verdict.
   Follow the project’s testing instructions when reviewing tests; run focused
   checks and reserve full suites for when they are necessary. Keep scoped files unchanged while review runs. Follow
   the current capacity and recovery rules; report the actual reviewer model.
   A timeout or failed run is not approval.
3. **Resolve findings autonomously.** Keep a ledger in the current thread with
   each ID, severity, evidence and outcome: fixed, disputed or declined. Verify
   each claim; apply the smallest justified in-scope fix without another routine approval stop.
   Reject false positives with evidence and decline optional or out-of-scope
   suggestions with a reason. Judge severity by impact and reachable behavior;
   rare security, data-loss and concurrency failures can still block completion.
   Run affected checks after fixes. Scope or authority changes still require
   the applicable approval.
4. **Re-review changed behavior.** Default to at most three completed review
   rounds. Extend automatically to five for security, permissions, auth, data
   loss or state/concurrency while evidenced required findings remain open, or
   as the user requests. Each new child gets the original brief, same base/scope,
   ledger, prior findings and responses, unresolved objections, full current
   diff and changes since the last round. Later rounds inspect changed behavior
   and open IDs, marking each resolved or still open. Request another round when
   behavior changed or required findings remain disputed. Declined nits and
   fixes that leave behavior unchanged need no further round. Changes to agent
   instructions count as behavior changes when they alter what the agent does.
5. **Close on evidence.** Finish when the reviewer approves the current behavior
   diff, required findings are resolved, relevant checks pass and the
   orchestrator has no outstanding concern. A round with only optional nits can
   close regardless of its verdict label once the orchestrator verifies no
   required findings or concerns remain; record that disposition rather than
   claiming reviewer approval. If a required finding stays disputed after two
   responses, the budget ends without agreement, or required review cannot run
   after authorized recovery, report the unresolved risk, evidence and smallest
   decision the user needs to make. Continue independent work within scope; never
   treat exhausted rounds or unavailable review as approval.
6. **Hand off or publish within authority.** Keep publication until review
   closes, then continue already-authorized commit, push or draft-PR work
   without another approval stop. Review grants no merge or production authority
   and never overrides project holds. Report rounds, actual model, checks,
   fixed/declined findings, remaining limits and publication status concisely.
