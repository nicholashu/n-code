"""Emit a short intake reminder only for a positively identified main thread."""

import json
from pathlib import Path
import sqlite3
import sys


def main():
    event = json.load(sys.stdin)
    if event.get('hook_event_name') != 'UserPromptSubmit':
        return
    home = Path.home()
    with sqlite3.connect((home / '.codex/state_5.sqlite').as_uri() + '?mode=ro', uri=True, timeout=0.2) as db:
        thread = db.execute('SELECT source, originator FROM threads WHERE id = ?',
                            (event.get('session_id'),)).fetchone()
    if not thread or thread[0] not in ('cli', 'vscode', 'exec') or thread[1] != 'T3 Code':
        return
    # T3 children also look like root Codex sessions; check app-owned lineage.
    with sqlite3.connect((home / '.t3/userdata/statev2.sqlite').as_uri() + '?mode=ro', uri=True, timeout=0.2) as db:
        rows = db.execute('''
            SELECT t.payload_json
            FROM orchestration_v2_projection_provider_threads p
            JOIN orchestration_v2_projection_threads t ON t.thread_id = p.thread_id
            WHERE json_extract(p.payload_json, '$.nativeThreadRef.nativeId') = ?
        ''', (event.get('session_id'),)).fetchall()
    if len(rows) != 1:
        return
    lineage = json.loads(rows[0][0]).get('lineage', {})
    if 'relationshipToParent' not in lineage or lineage['relationshipToParent'] not in (None, 'fork'):
        return
    skill = home / '.codex/skills/prompt-check/SKILL.md'
    print(f'For a new user task, apply {skill} before implementation or delegation. '
          'Check goal, acceptance proof, deliverables and relevant boundaries; ask only for '
          'consequential missing information that cannot be inferred. Skip simple or clear requests. '
          'For ongoing tasks, reassess only material scope changes. Continue the original task; '
          'never return a rewritten prompt. Keep this check internal unless clarification is needed.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, sqlite3.Error, ValueError, TypeError, AttributeError):
        # Unknown identity or schema drift must never inject into a possible child.
        pass
