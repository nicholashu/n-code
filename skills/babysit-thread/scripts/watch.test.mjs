import assert from 'node:assert/strict';
import test from 'node:test';
import { reportable } from './watch.mjs';

const shell = (id, changes = {}) => ({
    id,
    latestRunId: 'run:' + id,
    status: 'completed',
    pendingRuntimeRequest: null,
    pendingBackgroundTasks: [],
    ...changes,
});
const observe = (...rows) => reportable(new Map(rows.map(row => [row.id, row])), 'parent', 'run:parent');

test('a finished parent remains active until awaited work clears', () => {
    assert.equal(observe(shell('parent', { pendingBackgroundTasks: [
        { kind: 'subagent', childThreadId: 'child' },
    ] }), shell('child', { status: 'running' })), null);
    assert.deepEqual(observe(shell('parent', { pendingBackgroundTasks: [
        { kind: 'command', taskId: 'dev-server' },
    ] })), { state: 'completed' });
});

test('an approval on an awaited child wakes the originating watch', () => {
    assert.deepEqual(observe(shell('parent', { pendingBackgroundTasks: [
        { kind: 'subagent', childThreadId: 'child' },
    ] }), shell('child', { pendingRuntimeRequest: { kind: 'command_execution' } })), {
        state: 'needs-attention', requestThreadId: 'child',
    });
});

test('work in another thread cannot wake the watch', () => {
    assert.equal(observe(shell('parent', { activityRunStatus: 'running' }),
        shell('unrelated', { pendingRuntimeRequest: { kind: 'user_input' } })), null);
});

test('a replacement run asks the PM to check ownership before closing', () => {
    assert.deepEqual(observe(shell('parent', { latestRunId: 'run:replacement' })), {
        state: 'run-changed', observedRunId: 'run:replacement',
    });
    assert.deepEqual(observe(shell('parent', { status: 'failed' })), { state: 'failed' });
});
