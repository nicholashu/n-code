---
name: babysit-thread
description: Watch an existing T3 Code thread until the work is done or someone needs to act. Use when asked to babysit or follow a T3 thread. Use babysit-pr for PR checks and reviews if installed.
---

# Babysit a T3 thread

## Find the thread

Use the thread link or task tracker to identify the thread and its T3 environment. Read the thread. Record its link, owner, run ID, expected result, and any required delegated results, reviews, or approvals. Use the owner's existing handoff and keep one watcher per thread.

For a status check, report what you find and stop. If asked to watch, continue until you verify the handoff or find a blocker that needs action.

## Answer questions and handle permissions

Check for questions and permission requests before waiting and when you review a paused thread. Answer routine questions within the agreed work using verified context. Use `pending_request` to read and answer structured questions when T3 exposes it. Reply to chat questions in the owning thread if authorized. Ask the requester for decisions that require their input. Include the thread link and the exact question.

Use the platform's approval control only if the exact action and target are already authorized and your role can approve them. `pending_request` handles questions only. If the approval control is unavailable to you or the request needs another approver, leave it pending and give the approver the thread link, action, and target. Verify the platform accepted a response before resuming the watch.

## Wait for completion

When T3 exposes `thread_wait`, pass the `environmentId`, `threadId`, and `runId` for the work you are watching. Set `untilDelegatedWorkSettled: true` if the result depends on delegated or background work.

Check `next` first. If it says T3 will wake the watching thread, keep the watched thread open and end your turn. Resume on the notification, including when the wait returned `timedOut: true`.

`timedOut: true` means the wait window elapsed. Use the run's status and evidence to determine the work's outcome. If a timeout has no `next` message, continue the native wait for the same run where supported. If you cannot wait or receive a notification, use the owner's existing handoff or arrange a permitted follow-up. Report the last verified status if neither is available.

For other wait results, read the thread before deciding what happened. Avoid polling, recurring checks, and extra watcher agents.

## Verify the handoff and settle

On wake, re-read the thread, the watched and latest runs, and the tracker if there is one. The run can finish while delegated work or required review is still pending. Follow a replacement run only if it continues the same work. Check for an active or queued replacement before considering recovery from a failed or interrupted run.

Keep active, blocked, and approval-pending threads open. Report the blocker, who can resolve it, and what they need to do. A watch grants no authority to restart, merge, release, or approve.

Verify the result against the agreed scope and confirm that the owner recorded the handoff. Ask delegated agents to settle their own threads after recording the handoff. Settlement of your own thread takes effect at turn end, so the lead checks for `settled: true` after the turn ends.

If a finished delegated thread is still open, ask its owner to settle it or use `thread_organize` with `action: settle` when authorized. Read the state back before reporting settlement. Leave user-started threads under the user's control. Link the thread and evidence in your report.
