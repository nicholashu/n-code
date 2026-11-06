# Choose workers

Use `gpt-6.1-sol` as the orchestrator. It scopes work, assigns workers, integrates results and decides whether evidence is sufficient. A skill cannot change the current thread's model; if it differs, disclose that and use supported model selection rather than claiming to be Sol.

Default to provider `codex`:

- `gpt-6.1-terra`, with `options:{reasoningEffort:"xhigh"}`, for bounded implementation, focused tests and investigation.
- `gpt-6.1-sol` for complex work and independent review when warranted.

Use these defaults without a provider questionnaire. The user can override models or providers for a task. Resolve IDs against the live catalog and follow the runtime's delegation rules; do not silently substitute an unavailable model.

When requested, Ollama Cloud and OpenCode Free remain available. For Ollama Cloud, allow at most three concurrent runs across parents and children. For OpenCode Free, select a live model explicitly labelled free, preferring GLM Flash or DeepSeek Flash. Respect all provider, host and app capacity limits.

On rate limits, queue work or report the blocked path and continue independent work. Switch models or providers only within the user's explicit fallback choices and the runtime's rules. Skip failed, unavailable, already-attempted or cooling-down candidates.
