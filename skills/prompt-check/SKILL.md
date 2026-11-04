---
name: prompt-check
description: Use in the main orchestrator after receiving an initial task, before implementation or delegation. Quickly check whether missing goals, acceptance criteria, deliverables or boundaries need clarification; ask only when consequential. Skip simple or already clear requests.
---

# Prompt Check

This is an orchestrator intake check, not a prompt-writing task. Assess once per new task; reassess later steering only if it materially changes scope or success. Missing headings are not missing intent. Never return a rewritten prompt, filled-in template or scored assessment.

## Decide quickly

Only the main orchestrator performs this check. Delegated agents follow their supplied brief without repeating intake. The local `UserPromptSubmit` hook in `scripts/hook.py` emits a short reminder only after verifying T3 main-thread lineage; unknown identities receive no context. It uses read-only local Codex/T3 metadata, whose schemas may change.

Use the prompt and already-loaded context. Do not research, inspect repositories, call other skills or delegate just to assess the prompt. A clarification tool is fine when available.

- **Clear and small:** A typo fix, explicit rename, translation, direct question or narrowly specified reversible edit usually needs no interview or formal contract. Proceed silently. Judge ambiguity and consequences, not prompt length: “delete old records” still needs a clear selection rule.
- **Enough to infer:** Infer obvious goals, deliverables and checks. Do not ask the user to supply test commands or implementation details the agent can discover during normal work. State only consequential assumptions, briefly, then proceed.
- **Material gap:** Ask when plausible answers would change the result, scope, preservation requirements or evidence needed to call it done. Ask before dependent implementation; continue independent authorized work if useful.

## Check only what matters

- **Goal:** What observable outcome is wanted? Ask only if competing interpretations matter; do not demand a business rationale for an obvious change.
- **Acceptance:** What condition would pass or fail? Prefer an input/action and expected result, a measurable threshold, or a concrete visual state. “Tests pass,” “works,” and “100% assertions” alone do not define the intended behavior. Propose a check grounded in the request; clarify unresolved product choices instead of inventing them. Let the agent find real commands later.
- **Deliverable:** What must be handed over, and at what completion stage? Infer the natural artifact. Clarify implementation versus proposal, local result versus deployed result, or other consequential ambiguity. This check grants no release authority.
- **Boundaries:** Ask about preserved behavior, compatibility or non-goals only when a plausible change would put them at risk. Honor existing constraints; do not fabricate restrictions, exact file lists or a legacy-support decision for every task.

Ask one short batch, usually one question and at most three. Include a concrete suggested answer when helpful. Ask only unresolved, consequential questions; avoid repeating answered ones or turning replies into a checklist interview. An unanswered necessary question remains open.

## Continue the original task

Keep the checklist internal. For each item, decide whether it is stated, safely inferable, unnecessary for this task, or consequentially missing. Only the last category warrants a clarification question. Missing acceptance criteria do not automatically mean the user must supply them: infer suitable proof from clear requested behavior.

If no necessary clarification remains, continue the authorized task without a separate assessment response. Otherwise ask the targeted question, use the reply as task context and resume once the material gap is resolved. Do not ask the user to approve a new brief or resubmit their request. Preserve the original task and its authorization; assessing quoted or hypothetical requests does not authorize executing them.

Keep clarification under about 150 words. Skip framework explanations, boilerplate and guarantees of first-run success.
