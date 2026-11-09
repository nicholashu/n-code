# n-code

## Skills

- `explain-clearly` guides clear technical explanations.
- `prompt-check` checks whether a task has consequential missing details before work begins. Its optional hook is specific to Codex running in T3 Code and uses local, read-only metadata; it fails closed if identity or database schemas cannot be verified. Installing the skill does not enable the hook.
- `t3-orchestration` guides explicitly requested delegation and review in T3 Code. It defaults to Sol 6.1 coordinating Terra workers; use the current runtime's instructions and override models according to your permissions and capacity.
- `build-brief` applies when an agreed design needs an implementation brief with acceptance checks and delivery boundaries.
- `grill-to-pr` applies when a feature needs an interview, implementation, verification and a draft PR. Invoke it with `$grill-to-pr` and the feature idea.
- `t3-eval` applies when creating a skill, changing skill behavior or comparing prompts. It runs blinded evaluations and skips proofreading.
- `unslop` edits writing to remove stock AI phrasing while preserving meaning. Invoke it explicitly.

## Other skills used

These skills live in their own public repositories. Local versions may include adaptations.

- [grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling) — required interview dependency for `grill-to-pr`; an installed `grill-me` entry point also works. This repository does not bundle either interview skill.
- [writing-tests](https://github.com/aaronvanston/agent-skills/tree/main/skills/writing-tests) — choosing useful test coverage.
- [diagnosing-bugs](https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs) — investigating bugs systematically.
- [resolving-merge-conflicts](https://github.com/mattpocock/skills/tree/321658273cb1d20b76026717d027d505790106d4/skills/engineering/resolving-merge-conflicts) — resolving merge conflicts; linked to a historical revision because it was removed upstream.
- [writing-for-agents](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents) — writing instructions for agents.
- [skill-shaper](https://github.com/overment/skills/tree/main/skills/skill-shaper) — creating and refining skills.
- [file-pr](https://github.com/t3dotgg/tstack/tree/main/skills/file-pr) — preparing concise pull requests.

## Pstack provenance

`t3-eval` adapts Lauren Tan's [pstack](https://github.com/cursor/plugins/tree/2776ddd2355d6d6c8747d3964600f28daf62f049/pstack), revision `2776ddd2355d6d6c8747d3964600f28daf62f049`, for supported T3 tools. `unslop` retains its upstream writing rules, translating the invocation flag to Codex's `agents/openai.yaml`. Each directory includes the upstream MIT license. The former `t3-automate-me` adaptation has been removed.

The T3 adaptations expect the installed `skill-creator` and/or `writing-tests` guidance named in their instructions. These skills do not install dependencies or change the current thread's model.
