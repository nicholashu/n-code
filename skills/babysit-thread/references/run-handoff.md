# Check the return path after a T3 launch or resume

1. Re-read T3. Record the link, scope, expected handoff, environment and thread
   IDs, and the exact active or queued run ID. Check for pending questions,
   approvals, and work this run is waiting for. If the run has ended, check its
   latest state and handoff. Follow a replacement run only if it continues the
   same work.
2. Confirm how the owning conversation will resume for this run. Reuse the
   owner's confirmed return path if it covers this run. In T3, prefer
   `thread_wait` with `environmentId`, `threadId`, and `runId`. Set
   `untilDelegatedWorkSettled: true` when the result depends on delegated or
   background work. Rely on `next` only when it says the owning conversation
   will resume, even if `timedOut` is true. Outside T3, use a supported one-time
   wait or callback. Record the accepted wait or callback and the conversation
   it will resume.
3. If you can't confirm a return path, try one bounded `thread_wait` for the
   exact run, if available and you haven't tried it for that run. Re-read T3.
   If the run is still active, use one permitted follow-up with the exact IDs.
   If none is available, tell the requester that automatic follow-up is
   unavailable and give them the thread link, run ID, and last verified status.
   Leave active, blocked, and approval-pending work open. Use one watcher and
   avoid recurring checks.
4. When notified, check that the notification names the watched run. Re-read
   that run and the thread's latest run. Check questions, approvals, and
   required reviews. Check the evidence in both the parent handoff and the
   handoffs from child runs the parent was waiting for. If a replacement run
   continues the same work, confirm the old wait ended and repeat the checklist
   for the new run. If the scope changed, return ownership to the requester.
   Confirm the evidence meets the brief before reporting completion.
