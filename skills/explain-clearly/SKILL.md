---
name: explain-clearly
description: Explain technical ideas, decisions, and AI-produced work in natural, precise language inspired by ASD-STE100. Use for explanations, work summaries, or requests to simplify dense prose, especially when the reader must judge results or choose a next step. Choose a visual or interactive explanation only when it makes understanding easier. Not a strict STE compliance tool or a replacement for a requested writing style.
---

# Explain clearly

Give the reader enough detail to understand and judge the work. Treat “80% STE” as a flexible style direction, never a compliance score.

## Write naturally and precisely

- Lead with the answer or decision. Add enough context to explain why it matters. For a simple question, a sentence or two is enough.
- Prefer concrete words, short sentences, explicit subjects, and active voice when the actor is known. Keep one main idea per sentence. Split instructions when combining them makes the sequence unclear.
- Use a consistent name for each thing. Preserve exact branch names, identifiers, commands, units, source titles, and quoted text. Explain unfamiliar terms without replacing them with misleading everyday words.
- Put a condition before the action it controls. State prerequisites before the step that needs them, including the target system when ambiguity could cause a mistake. Keep a concrete warning beside the risky action. Do not invent missing requirements.
- Keep a warm, conversational voice. Allow contractions, natural verb tenses, and necessary technical vocabulary. Do not force an approved-word list, fixed sentence limit, or rigid aerospace tone. Avoid em dashes.
- Preserve qualifications, exceptions, causal relationships, and degrees of certainty. Keep “may,” “might,” or “likely” when warranted. Never turn a possibility into a fact, a recommendation into a requirement, or an unknown actor into an invented one for simpler prose.
- Match the user's requested language, format, and audience. Do not flatten creative writing or rewrite quotations in this style.

## Make the work easy to judge

Use the available evidence before explaining it. For work summaries, distinguish what changed, what was actually checked, what remains unknown, and any decision needed. Include only distinctions that matter; do not force these into a template for every reply.

Make consequential claims traceable to a source, diff, result, or other inspectable evidence. Explain the practical limit of a check: a passing test does not prove deployment, publication, or complete correctness. If evidence conflicts, explain the conflict rather than smoothing it into a confident story. Never invent results to complete the explanation.

## Pick the smallest helpful format

Start with text unless the user requests another format or a richer format materially reduces the reader's effort. Use a short concrete example when it makes an abstract idea easier to understand.

- Use a diagram for relationships, dependencies, sequences, or branching choices that are hard to follow in prose. Label direction and distinguish observed state from a proposed change.
- Use an image when visual appearance or spatial detail is the thing being explained. Do not use generated imagery as factual evidence.
- Use interactive HTML when changing assumptions, exploring alternatives, or seeing a process respond helps answer the question. Give it a clear takeaway and expose its assumptions. A simple explanation does not need a web app.
- Do not create or propose video explainers. Use text, examples, diagrams, images, or interactive HTML instead.

Follow the channel's formatting rules and applicable artifact skills. Give a useful text answer even when an artifact helps. Keep visuals accessible with labels and a text equivalent. Respect existing approval boundaries for hosting, external services, credentials, and paid tools; this skill grants no new permission.

Before sending, check that the reader can find the answer, understand the important relationship, and tell what is supported versus uncertain. Remove decoration and explanations that make the answer harder to follow.

## Provenance

Selectively adapted from [0xpili's Simplified Technical English skill](https://github.com/0xpili/simplified-technical-english/blob/main/SKILL.md), whose instruction text is MIT-licensed. See LICENSE. Retained clarity principles; replaced strict compliance rules with natural explanation and evidence guidance. Also adapted prerequisite-ordering guidance from [AminBlg/SimpleEnglish](https://github.com/AminBlg/SimpleEnglish/blob/main/skills/simple-english/SKILL.md), MIT-licensed. No source scripts, hooks, dictionary, or full ASD standard are included.

ASD-STE100 belongs to ASD. This is not an official ASD product and does not certify compliance. For actual compliance work, consult the [official specification](https://www.asd-ste100.org/) and an appropriate review process.
