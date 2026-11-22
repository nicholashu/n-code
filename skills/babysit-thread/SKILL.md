---
name: babysit-thread
description: Follow T3 Code work through its verified handoff. Use when asked to babysit a thread or when handing off, resuming, or replacing T3 work you own. Use babysit-pr for PR checks and reviews if installed.
---

# Babysit a T3 thread

## Find the thread

Use the thread link or task tracker to identify the thread and its T3 environment. Read the thread. Record its link, owner, run ID, expected result, and any required delegated results, reviews, or approvals. Use the owner's existing handoff and keep one watcher per thread.

For a status check, report what you find and stop. If you own the handoff after a launch or resume, or were asked to watch, apply the [run handoff checklist](references/run-handoff.md) before ending the turn. Repeat it for an active same-scope replacement.

## Answer questions and handle permissions

Check for questions and permission requests before waiting and when you review a paused thread. Answer routine questions within the agreed work using verified context. Use `pending_request` to read and answer structured questions when T3 exposes it. Reply to chat questions in the owning thread if authorized. Ask the requester for decisions that require their input. Include the thread link and the exact question.

Use the platform's approval control only if the exact action and target are already authorized and your role can approve them. `pending_request` handles questions only. If the approval control is unavailable to you or the request needs another approver, leave it pending and give the approver the thread link, action, and target. Verify the platform accepted a response before resuming the watch.

## Wait for completion

Use the return path confirmed by the [run handoff checklist](references/run-handoff.md). For an agent outside T3 that can register a one-shot wait on a local file, the [optional macOS watcher](references/local-watcher.md) writes the receipt without needing the agent host's credentials.

## Verify the handoff and settle

On wake, re-read the thread, the watched and latest runs, and the tracker if there is one. The run can finish while delegated work or required review is still pending. Follow a replacement run only if it continues the same work. Check for an active or queued replacement before considering recovery from a failed or interrupted run.

Keep active, blocked, and approval-pending threads open. Report the blocker, who can resolve it, and what they need to do. A watch grants no authority to restart, merge, release, or approve.

Verify the result against the agreed scope and confirm that the owner recorded the handoff.

### Collect the handoff retro

Before settling, ask the worker what slowed or blocked the work, what it cost,
what helped, and what they'd change next time. If possible, put the question in
the delegation brief so the answer comes with the handoff. Ask the lead to
include reports from child workers. "None" is fine. If the thread has settled, use the handoff
on record and leave the thread closed.

Tell the owner about urgent blockers as they happen. If the team has a feedback
channel, report each verified issue there once. Keep sensitive details in the
owning conversation.

### Settle and report

Ask delegated agents to settle their own threads after recording the handoff. Settlement of your own thread takes effect at turn end, so the lead checks for `settled: true` after the turn ends.

If a finished delegated thread is still open, ask its owner to settle it or use `thread_organize` with `action: settle` when authorized. Read the state back before reporting settlement. Leave user-started threads under the user's control. Link the thread and evidence in your report.
