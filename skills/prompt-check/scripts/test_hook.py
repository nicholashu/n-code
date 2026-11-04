import json
from pathlib import Path
import sqlite3
import subprocess
import tempfile
import unittest


class HookTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        (self.home / '.codex').mkdir()
        (self.home / '.t3/userdata').mkdir(parents=True)
        with sqlite3.connect(self.home / '.codex/state_5.sqlite') as db:
            db.execute('CREATE TABLE threads (id TEXT, source TEXT, originator TEXT)')
        with sqlite3.connect(self.home / '.t3/userdata/statev2.sqlite') as db:
            db.execute('CREATE TABLE orchestration_v2_projection_provider_threads (thread_id TEXT, payload_json TEXT)')
            db.execute('CREATE TABLE orchestration_v2_projection_threads (thread_id TEXT, payload_json TEXT)')

    def run_hook(self, source='vscode', originator='T3 Code', relationship=None, mapped=True):
        with sqlite3.connect(self.home / '.codex/state_5.sqlite') as db:
            db.execute('INSERT INTO threads VALUES (?, ?, ?)', ('native-1', source, originator))
        if mapped:
            with sqlite3.connect(self.home / '.t3/userdata/statev2.sqlite') as db:
                db.execute('INSERT INTO orchestration_v2_projection_provider_threads VALUES (?, ?)',
                           ('app-1', json.dumps({'nativeThreadRef': {'nativeId': 'native-1'}})))
                db.execute('INSERT INTO orchestration_v2_projection_threads VALUES (?, ?)',
                           ('app-1', json.dumps({'lineage': {'relationshipToParent': relationship}})))
        return subprocess.run(
            ['/usr/bin/python3', '-c',
             'import runpy,sys; from pathlib import Path; from unittest.mock import patch; '
             'p=patch.object(Path,"home",return_value=Path(sys.argv[1])); p.start(); runpy.run_path(sys.argv[2],run_name="__main__")',
             str(self.home), str(Path(__file__).with_name('hook.py'))],
            input=json.dumps({'hook_event_name': 'UserPromptSubmit', 'session_id': 'native-1'}),
            text=True, capture_output=True, timeout=3)

    def test_main_thread_receives_compact_skill_reminder(self):
        result = self.run_hook()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('prompt-check/SKILL.md', result.stdout)
        self.assertLess(len(result.stdout.split()), 100)

    def test_t3_child_receives_no_context(self):
        result = self.run_hook(relationship='subagent')
        self.assertEqual((result.returncode, result.stdout), (0, ''))

    def test_native_subagent_receives_no_context(self):
        result = self.run_hook(source=json.dumps({'subagent': {'spawn': {}}}), originator='codex', mapped=False)
        self.assertEqual((result.returncode, result.stdout), (0, ''))

    def test_unmapped_t3_thread_receives_no_context(self):
        result = self.run_hook(mapped=False)
        self.assertEqual((result.returncode, result.stdout), (0, ''))

    def test_unrecognized_originator_receives_no_context(self):
        result = self.run_hook(originator='Unknown launcher')
        self.assertEqual((result.returncode, result.stdout), (0, ''))


if __name__ == '__main__':
    unittest.main()
