# Use a local receipt to resume the owning chat

This optional watcher subscribes to the T3 desktop's local event stream on macOS. The receiving app must be able to accept a one-shot file wait on that same computer and resume the owning conversation. Check the conversation's authority and whether it already has a watcher before starting. If the app offers no such route, use the [handoff fallback](run-handoff.md).

## Start and register a return path

1. On the Mac running the T3 desktop, use Node.js 24 or later and the local T3 CLI. Run the bundled [`scripts/watch.mjs`](../scripts/watch.mjs) from the skill folder. The script uses `t3` from your `PATH` or the T3 data directory's `bin` folder. Use `--t3` and `--base` with absolute paths to override those defaults. The default data directory is `~/.t3`. Use `probe` with the environment, thread and run IDs to verify the subscription without creating a watch.

   ```sh
   node scripts/watch.mjs start \
     --environment ENVIRONMENT_ID --thread THREAD_ID --run RUN_ID \
     --result /absolute/path/to/new-receipt.json
   ```

2. After the script returns `started: true`, register one file-exists wait for that receipt in the owning conversation. Set its deadline after the watcher expires. The default watcher runs at most eight hours. In OpenMausBot, use `wait_until` with `kind: file_exists` and a nine-hour deadline. Supply a permitted follow-up with the receipt path, exact IDs, T3 link and expected handoff. Record the accepted wait ID and its destination before saying you will be notified.
3. If the receipt already exists, read and verify it now. If registration is refused, remove only the job you just started with `launchctl remove JOB_LABEL`, using the returned label, and verify it is gone. If registration is ambiguous, inspect existing waits once before deciding who owns the route. When the original route cannot be confirmed, use the [fallback](run-handoff.md#check-the-return-path-after-a-t3-launch-or-resume).

## Use the receipt

The receipt contains `environment`, `thread`, `run`, and a `state`. Compare the IDs to the job you registered. `run-changed` provides `observedRunId`. `needs-attention` provides `requestThreadId`. A terminal state or a `watch-*` error is a reason to re-read T3. None of these states authorizes acting on a request or establishes that the agreed handoff is complete.

For an active same-scope replacement, wait for the previous one-shot route to end or retire it using the owning app's supported controls, then arm the exact new run with a new receipt path. The script rejects overlapping jobs for the same environment and thread. Confirm any pre-existing watcher from another installation has finished before starting a new one.
