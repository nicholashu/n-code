#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import { createHash, randomUUID } from 'node:crypto';
import { accessSync, constants, existsSync, linkSync, mkdtempSync, readFileSync, realpathSync, rmSync, statSync, unlinkSync, writeFileSync } from 'node:fs';
import { homedir, tmpdir } from 'node:os';
import { delimiter, dirname, isAbsolute, join } from 'node:path';
import { setTimeout as delay } from 'node:timers/promises';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';

const launchctl = '/bin/launchctl';
const launchDomain = () => `gui/${process.getuid()}`;
const script = fileURLToPath(import.meta.url);
const idPattern = /^[A-Za-z0-9_.:@%-]{1,512}$/;
const uuidPattern = /^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$/i;
const terminal = new Set(['completed', 'failed', 'interrupted', 'cancelled', 'rolled_back']);
const hold = task => task.awaited === true || ['subagent', 'background_task'].includes(task.kind);

function command(path, args) {
    return execFileSync(path, args, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'],
        timeout: 15_000, maxBuffer: 768 * 1024 }).trim();
}

function t3Executable(explicit, base) {
    if (explicit && !isAbsolute(explicit)) throw new Error('--t3 must be an absolute executable path.');
    const candidates = explicit ? [explicit] : [
        ...(process.env.PATH ?? '').split(delimiter).filter(isAbsolute).map(folder => join(folder, 't3')),
        join(base, 'bin', 't3'),
    ];
    for (const candidate of candidates) {
        try {
            accessSync(candidate, constants.X_OK);
            if (statSync(candidate).isFile()) return candidate;
        } catch {
            // Try the next configured location.
        }
    }
    throw new Error('T3 CLI is unavailable. Supply its absolute path with --t3.');
}

function startJob(label, args) {
    const directory = mkdtempSync(join(tmpdir(), 't3-thread-watch-'));
    const plist = join(directory, `${label}.plist`);
    const xmlString = value => `<string>${value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;')}</string>`;
    const program = [process.execPath, script, 'run', ...args].map(xmlString).join('');
    try {
        writeFileSync(plist, `<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict>
<key>Label</key>${xmlString(label)}<key>ProgramArguments</key><array>${program}</array><key>RunAtLoad</key><true/>
</dict></plist>`, { mode: 0o600, flag: 'wx' });
        command(launchctl, ['bootstrap', launchDomain(), plist]);
    } catch (error) {
        if (error.cmd) {
            try {
                command(launchctl, ['print', `${launchDomain()}/${label}`]);
            } catch {
                throw error;
            }
            throw new Error('A watcher already owns this T3 thread. Reuse its confirmed return path or use the fallback.');
        }
        throw error;
    } finally {
        rmSync(directory, { recursive: true, force: true });
    }
}

function readLocalT3(options) {
    const state = join(options.base, 'userdata');
    if (readFileSync(join(state, 'environment-id'), 'utf8').trim() !== options.environment) {
        throw new Error('The requested T3 environment does not match this Mac.');
    }
    const url = new URL(JSON.parse(readFileSync(join(state, 'server-runtime.json'), 'utf8')).origin);
    if (url.href !== `${url.origin}/` || url.protocol !== 'http:' || !['127.0.0.1', '[::1]'].includes(url.hostname)) {
        throw new Error('The local T3 server must have a loopback address.');
    }
    return url;
}

function writeReceipt(path, receipt) {
    const temp = path + '.' + randomUUID();
    writeFileSync(temp, JSON.stringify(receipt) + '\n', { mode: 0o600, flag: 'wx' });
    try {
        linkSync(temp, path);
    } finally {
        unlinkSync(temp);
    }
}

export function reportable(threads, threadId, runId) {
    const root = threads.get(threadId);
    if (!root) return { state: 'thread-unavailable' };
    const seen = new Set();
    const waiting = [root];
    while (waiting.length) {
        const thread = waiting.pop();
        if (seen.has(thread.id)) continue;
        seen.add(thread.id);
        const request = thread.pendingRuntimeRequest;
        if (request && request.kind !== 'dynamic_tool_call') {
            return { state: 'needs-attention', requestThreadId: thread.id };
        }
        for (const task of thread.pendingBackgroundTasks ?? []) {
            const child = threads.get(task.childThreadId);
            if (hold(task) && child) waiting.push(child);
        }
    }
    const background = root.pendingBackgroundTasks ?? [];
    if (root.blockedOnThreadWait || background.some(hold)
        || (root.latestRunBackgroundWake && background.some(task =>
            task.kind === 'monitor' && !task.taskId?.startsWith('pull-request-watch:')))) return null;
    if (root.latestRunId !== runId) {
        return root.latestRunId ? { state: 'run-changed', observedRunId: root.latestRunId } : null;
    }
    const status = root.activityRunStatus ?? root.status;
    return terminal.has(status) ? { state: status } : null;
}

function subscribe(url, token, options, deadline, signal) {
    return new Promise((resolve, reject) => {
        const socketUrl = new URL('/ws?orchestrationProtocol=2', url);
        socketUrl.protocol = 'ws:';
        const ws = new WebSocket(socketUrl, { headers: { Authorization: 'Bearer ' + token } });
        const threads = new Map();
        let initialized = false;
        let lastFrame = Date.now();
        let finished = false;
        const timer = setInterval(() => {
            const now = Date.now();
            if (now >= deadline) finish({ state: 'watch-expired' });
            else if (now - lastFrame > (initialized ? 65_000 : 15_000)) finish(null);
            else if (ws.readyState === WebSocket.OPEN) send({ _tag: 'Ping' });
        }, 5_000);
        const finish = (result, error) => {
            if (finished) return;
            finished = true;
            clearInterval(timer);
            signal?.removeEventListener('abort', cancel);
            ws.close();
            if (error) reject(error);
            else resolve({ result, initialized });
        };
        const cancel = () => finish({ state: 'watch-cancelled' });
        const send = message => ws.send(JSON.stringify(message));

        signal?.addEventListener('abort', cancel, { once: true });
        ws.addEventListener('open', () => send({ _tag: 'Request', id: '1', headers: [],
            tag: 'orchestration.subscribeShell', payload: { requestCompletionMarker: true } }));
        ws.addEventListener('close', () => finish(null));
        ws.addEventListener('error', () => finish(null));
        ws.addEventListener('message', ({ data }) => {
            try {
                lastFrame = Date.now();
                const frame = JSON.parse(data);
                if (frame._tag === 'Exit' || frame._tag === 'Defect') {
                    throw new Error('T3 refused the event subscription.');
                }
                if (frame._tag !== 'Chunk' || frame.requestId !== '1') return;
                send({ _tag: 'Ack', requestId: '1' });
                for (const item of frame.values) {
                    if (item.kind === 'snapshot') {
                        const rows = [...item.snapshot.threads, ...item.snapshot.archivedThreads];
                        for (const row of rows) threads.set(row.id, row);
                    } else if (item.kind === 'thread.updated') {
                        threads.set(item.thread.id, item.thread);
                    } else if (item.kind === 'thread.removed') {
                        threads.delete(item.threadId);
                    } else if (item.kind === 'synchronized') {
                        initialized = true;
                    }
                }
                if (!initialized) return;
                const outcome = reportable(threads, options.thread, options.run);
                if (options.probe) finish({ state: 'subscribed', observed: outcome?.state ?? 'working' });
                else if (outcome) finish(outcome);
            } catch {
                finish(null, new Error('T3 did not provide a usable event stream.'));
            }
        });
    });
}

async function watch(options, signal) {
    readLocalT3(options);
    const ttl = (options.probe ? 5 : (Number(options.hours) + 1) * 60) + 'm';
    const credential = JSON.parse(command(options.t3, ['auth', 'session', 'issue', '--base-dir',
        options.base, '--scope', 'orchestration:read', '--ttl', ttl, '--label', 'T3 thread watcher', '--json']));
    if (!credential.token || !credential.sessionId) throw new Error('T3 did not issue read access.');
    try {
        const deadline = Date.now() + (options.probe ? 15_000 : Number(options.hours) * 3_600_000);
        let consecutiveFailures = 0;
        while (Date.now() < deadline) {
            if (signal?.aborted) return { state: 'watch-cancelled' };
            const { result, initialized } = await subscribe(readLocalT3(options),
                credential.token, options, deadline, signal);
            if (result) return result;
            consecutiveFailures = initialized ? 0 : consecutiveFailures + 1;
            if (consecutiveFailures >= 4 || options.probe) return { state: 'watch-disconnected' };
            await delay(Math.min(1_000 * 2 ** consecutiveFailures, 10_000), undefined, { signal });
        }
        return { state: 'watch-expired' };
    } finally {
        try {
            command(options.t3, ['auth', 'session', 'revoke', '--base-dir', options.base, credential.sessionId]);
        } catch {
            // This revocation failure leaves a short-lived read-only credential.
        }
    }
}

async function main() {
    const [action, ...args] = process.argv.slice(2);
    if (!['start', 'run', 'probe'].includes(action)) {
        console.log('Usage: node watch.mjs start|probe --environment ID --thread ID --run ID [--result ABSOLUTE_PATH] [--hours 1-24] [--t3 ABSOLUTE_PATH] [--base ABSOLUTE_PATH]');
        if (action !== '--help') process.exitCode = 1;
        return;
    }
    const major = Number(process.versions.node.split('.')[0]);
    if (major < 24) throw new Error('Use Node.js 24 or later.');
    if (process.platform !== 'darwin') throw new Error('The receipt watcher runs on a macOS T3 desktop.');
    const { values: options } = parseArgs({ args, options: {
        environment: { type: 'string' }, thread: { type: 'string' }, run: { type: 'string' },
        result: { type: 'string' }, hours: { type: 'string', default: '8' }, t3: { type: 'string' },
        base: { type: 'string', default: join(homedir(), '.t3') },
    } });
    if (!uuidPattern.test(options.environment ?? '') || !idPattern.test(options.thread ?? '')
        || !idPattern.test(options.run ?? '') || !/^(?:[1-9]|1[0-9]|2[0-4])$/.test(options.hours)
        || !isAbsolute(options.base) || (action !== 'probe' && !isAbsolute(options.result ?? ''))) {
        throw new Error('Supply the exact T3 environment, thread and run, absolute file paths, and 1–24 hours.');
    }
    options.t3 = t3Executable(options.t3, options.base);
    if (action === 'probe') {
        options.probe = true;
        const result = await watch(options);
        console.log(JSON.stringify(result));
        if (result.state !== 'subscribed') process.exitCode = 1;
        return;
    }

    const label = 't3.thread-watch.' + createHash('sha256')
        .update(options.environment + '/' + options.thread).digest('hex').slice(0, 24);
    if (existsSync(options.result)) throw new Error('Choose a new result path for this watch.');
    if (action === 'start') {
        readLocalT3(options);
        accessSync(dirname(options.result), constants.W_OK);
        // Launchd may have a different PATH and home from the shell that started the job.
        const workerArgs = Object.entries(options).flatMap(([name, value]) => [`--${name}`, value]);
        startJob(label, workerArgs);
        console.log(JSON.stringify({ started: true, label, result: options.result, delivery: 'file' }));
        return;
    }
    const stop = new AbortController();
    const cancel = () => stop.abort();
    process.once('SIGTERM', cancel);
    try {
        let outcome;
        try {
            outcome = await watch(options, stop.signal);
        } catch {
            outcome = { state: 'watch-unavailable' };
        }
        if (!stop.signal.aborted) {
            writeReceipt(options.result, { ...outcome, environment: options.environment, thread: options.thread, run: options.run });
        }
    } finally {
        process.removeListener('SIGTERM', cancel);
        if (!stop.signal.aborted) {
            try { command(launchctl, ['remove', label]); } catch { /* The job may already be gone. */ }
        }
    }
}

if (process.argv[1] && existsSync(process.argv[1]) && realpathSync(process.argv[1]) === script) {
    main().catch(error => {
        // Child CLI output and socket data can contain credentials or transcript text.
        console.error(error.constructor === Error && !error.code && !error.cmd
            ? error.message : 'Could not run the T3 watcher. Check the local CLI, desktop session, and receipt directory.');
        process.exitCode = 1;
    });
}
