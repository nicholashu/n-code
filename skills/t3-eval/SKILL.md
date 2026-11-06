---
name: t3-eval
description: Run blinded behavioral evaluations of agent skills or prompts in T3 when asked to test their effectiveness or compare variants.
---

# Evaluate agent behavior

Run ordinary tasks and grade observable decisions and artifacts. Reading instructions or checking their format does not prove behavior.

## Design

- Read the installed writing-tests skill. Choose realistic tasks that expose distinct failures, including an error or permission boundary. Set three to six observable criteria before running anything. Define required gates that cannot be averaged away.
- For a comparison, hold tasks, fixtures, models, settings and tool access constant; vary the instruction under study. Repeat cases when reliability matters. Record revisions, settings and attempts, including failures and dropouts.
- Keep the rubric, variant mapping and results outside candidate workspaces. Give candidates ordinary project names and user requests. Do not announce the evaluation, other candidates or expected decisions. Do not ask them to list which instructions they followed.

## Run

- Use fresh agents without inherited evaluation conversation. Follow the current runtime's delegation rules. Use native children when eligible; use T3 delegation for requested settings, other providers or worktree isolation. Let T3 create delegated worktrees. Do not make top-level threads unless requested.
- Give each run its own writable scope and identical task fixtures. Supply the skill as an ordinary available instruction, with its real dependencies. Keep grading files inaccessible through the granted tools where possible; report shared-filesystem or inherited-context leakage when isolation cannot enforce this.
- Default to the model intended to use the skill. Resolve requested models live; never silently substitute. Apply real task permissions to fixtures too. Do not publish, contact others or touch production as part of an evaluation without specific authority.
- Let candidates act. Collect supported task results, transcripts, diffs and runtime artifacts. Follow completion notifications rather than polling. Do not coach a failing run; record corrections as separate attempts. Label simulated events explicitly in the report.

## Judge

- Give a fresh judge neutral output labels and the rubric, without model or variant identities. Prefer a different model family only when authorized and available; otherwise disclose the same-family limitation. Remove identifying metadata without altering behavioral evidence.
- Grade each criterion PASS, FAIL or NOT OBSERVED with evidence. Missing evidence is not a pass. Verify consequential claims against artifacts or tool records, not candidate self-report. Read every result and resolve disagreements with evidence.
- Separate instruction failures, fixture defects and unavailable runtime capabilities. Do not change criteria after seeing results to make a variant pass.

**Reply:** cases and attempts, evidence-backed verdicts, blinding limits, real versus simulated execution, and the recommendation. Evaluation grants no authority to install or publish the variant.
