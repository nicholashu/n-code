# n-code

## Skills

- [`create-yoto-story`](skills/create-yoto-story/SKILL.md) creates independent Yoto story cards, with bundled GIF, cover, Fish/local speech, upload and playlist tools. Requires Python 3, Pillow, msgpack and ffmpeg; account operations use your own Yoto credentials.

- `explain-clearly` guides clear technical explanations.
- `prompt-check` checks whether a task has consequential missing details before work begins. Its optional hook is specific to Codex running in T3 Code and uses local, read-only metadata; it fails closed if identity or database schemas cannot be verified. Installing the skill does not enable the hook.
- `t3-orchestration` coordinates substantial tasks in T3 Code when independent work or specialist review would help. The current model coordinates Terra workers. Follow the current runtime's delegation rules and override worker models according to your permissions and capacity.
- `build-brief` applies when an agreed design needs an implementation brief with acceptance checks and delivery boundaries.
- `grill-to-pr` applies when a feature needs an interview, implementation, verification and a draft PR. Invoke it with `$grill-to-pr` and the feature idea.
- `t3-eval` applies when creating a skill, changing skill behavior or comparing prompts. It runs blinded evaluations and skips proofreading.
- `unslop` edits writing to remove stock AI phrasing while preserving meaning. Invoke it explicitly.
- [`babysit-thread`](skills/babysit-thread/SKILL.md) follows a T3 Code thread through its final handoff. It covers waiting, questions, permissions, and settlement.
- [`file-pr`](skills/file-pr/SKILL.md) files pull requests with evidence suited to the change and covers adding and verifying media in PR descriptions and comments. It adapts [tstack’s file-pr](https://github.com/t3dotgg/tstack/tree/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/file-pr) under the [MIT license](skills/file-pr/LICENSE).

## Other skills used

These skills live in their own public repositories. Local versions may include adaptations.

- [grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling) — required interview dependency for `grill-to-pr`; an installed `grill-me` entry point also works. This repository does not bundle either interview skill.
- [writing-tests](https://github.com/aaronvanston/agent-skills/tree/main/skills/writing-tests) — choosing useful test coverage.
- [diagnosing-bugs](https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs) — investigating bugs systematically.
- [resolving-merge-conflicts](https://github.com/mattpocock/skills/tree/321658273cb1d20b76026717d027d505790106d4/skills/engineering/resolving-merge-conflicts) — resolving merge conflicts; linked to a historical revision because it was removed upstream.
- [writing-for-agents](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents) — writing instructions for agents.
- [skill-shaper](https://github.com/overment/skills/tree/main/skills/skill-shaper) — creating and refining skills.

## Pstack provenance

`t3-eval` adapts Lauren Tan's [pstack](https://github.com/cursor/plugins/tree/2776ddd2355d6d6c8747d3964600f28daf62f049/pstack), revision `2776ddd2355d6d6c8747d3964600f28daf62f049`, for supported T3 tools. `unslop` retains its upstream writing rules, translating the invocation flag to Codex's `agents/openai.yaml`. Each directory includes the upstream MIT license. The former `t3-automate-me` adaptation has been removed.

The T3 adaptations expect the installed `skill-creator` and/or `writing-tests` guidance named in their instructions. These skills do not install dependencies or change the current thread's model.
