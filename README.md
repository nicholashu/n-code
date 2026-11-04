# n-code

## Skills

- `explain-clearly` guides clear technical explanations.
- `prompt-check` checks whether a task has consequential missing details before work begins. Its optional hook is specific to Codex running in T3 Code and uses local, read-only metadata; it fails closed if identity or database schemas cannot be verified. Installing the skill does not enable the hook.
- `t3-orchestration` guides explicitly requested delegation and review in T3 Code. Use the current runtime's instructions and configure providers according to your own permissions and capacity.

## Other skills used

These skills live in their own public repositories. Local versions may include adaptations.

- [writing-tests](https://github.com/aaronvanston/agent-skills/tree/main/skills/writing-tests) — choosing useful test coverage.
- [diagnosing-bugs](https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs) — investigating bugs systematically.
- [resolving-merge-conflicts](https://github.com/mattpocock/skills/tree/321658273cb1d20b76026717d027d505790106d4/skills/engineering/resolving-merge-conflicts) — resolving merge conflicts; linked to a historical revision because it was removed upstream.
- [writing-for-agents](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents) — writing instructions for agents.
- [skill-shaper](https://github.com/overment/skills/tree/main/skills/skill-shaper) — creating and refining skills.
- [file-pr](https://github.com/t3dotgg/tstack/tree/main/skills/file-pr) — preparing concise pull requests.
