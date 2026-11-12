# Choose workers

The model running this skill is the orchestrator, regardless of which model it is. Scope the work, assign workers, integrate results and assess evidence in the current thread. Worker model defaults below do not require changing the orchestrator's model or creating an orchestrator child. Give workers bounded tasks and have them return results directly. They may delegate further only if their brief authorizes it and the current runtime permits it.

Default to provider `codex`:

- `gpt-6.1-terra`, with `options:{reasoningEffort:"xhigh"}`, for bounded implementation, focused tests and investigation.
- `gpt-6.1-sol` for complex work and independent review when warranted.

Use these defaults without asking the user to choose a provider. The user can override models or providers for a task. Resolve IDs against the live catalog and follow the runtime's delegation rules; do not silently substitute an unavailable model.

When requested, use Ollama Cloud or OpenCode Free. For Ollama Cloud, allow at most three concurrent runs across parents and children. For OpenCode Free, select a live model explicitly labelled free, preferring GLM Flash or DeepSeek Flash. Respect all provider, host and app capacity limits.

If a rate limit blocks a run, queue it or report the blocker and continue independent work. Switch models or providers only within the user's explicit fallback choices and the runtime's rules. Skip failed, unavailable, already-attempted or cooling-down candidates.
