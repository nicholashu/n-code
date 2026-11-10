import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image
import yoto_media as media


class MediaTests(unittest.TestCase):
    def test_export_keeps_pixels_timing_and_clears_previous_frame(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            frames = []
            expected = []
            for i in range(3):
                im = Image.new('RGBA', (16, 16))
                im.putpixel((i, 0), (255, 0, 0, 255))
                path = root / f'{i}.png'
                im.save(path); frames.append(path)
                rgb = Image.new('RGB', (16, 16)); rgb.putpixel((i, 0), (255, 0, 0))
                expected.append(rgb.tobytes())
            output = root / 'icon.gif'
            media.gif(frames, output, [120, 80, 160])
            with Image.open(output) as im:
                actual = []
                for i in range(im.n_frames):
                    im.seek(i)
                    actual.append((im.convert('RGB').tobytes(), im.info['duration']))
            self.assertEqual(actual, list(zip(expected, [120, 80, 160])))

    def test_existing_receipt_prevents_network_even_for_uncertain_create(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            receipt = root / 'card.json'
            receipt.write_text('{"status":"create_pending"}')
            with patch('sys.argv', ['media', 'publish-new', str(root/'payload.json'), str(receipt), '--sha256', 'abc']), patch.object(media, 'request') as network, contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(media.main(), 1)
            network.assert_not_called()
            self.assertEqual(json.loads(receipt.read_text())['status'], 'create_pending')

    def test_new_receipt_name_cannot_bypass_project_pending_create(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root/'build').mkdir()
            (root/'card.json').write_text('{"status":"create_pending"}')
            alternate = root/'another-card.json'
            with patch('sys.argv', ['media', 'publish-new', str(root/'build/content.json'), str(alternate), '--sha256', 'abc']), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(media.main(), 1)
            self.assertFalse(alternate.exists())

    def test_local_rejects_non_loopback_before_sending_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); text = root/'scene.txt'; text.write_text('Hello')
            with patch('sys.argv', ['media', 'speech', str(text), str(root/'scene.mp3'), '--voice', 'narrator', '--local', 'http://example.com']), patch.object(media, 'request') as network, contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(media.main(), 1)
            network.assert_not_called()
            self.assertFalse((root/'scene.mp3').exists())

    def test_speech_rejects_non_audio_response_without_saving_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); text = root/'scene.txt'; text.write_text('Hello')
            args = type('Args', (), dict(text=text, output=root/'scene.mp3', voice='narrator', model=None, local='http://127.0.0.1:8080'))()
            with patch.object(media, 'request', return_value=b'{"error":"not audio"}'):
                with self.assertRaises(Exception):
                    media.speech(args)
            self.assertFalse(args.output.exists())
            self.assertFalse(Path(str(args.output) + '.source.json').exists())

    def test_cover_preserves_entire_composition(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root/'poster.png'; output = root/'upload.png'
            Image.new('RGB', (1000, 1000), 'red').save(source)
            media.cover(source, output)
            with Image.open(output) as im:
                self.assertEqual(im.size, (600, 825))
                self.assertEqual(im.getpixel((300, 412)), (255, 0, 0))
                self.assertEqual(im.getpixel((0, 0)), (0, 0, 0))


class IndependentProjectTests(unittest.TestCase):
    def prepare(self, root):
        media.new_project(root, 'Woodland bell')
        manifest = json.loads((root/'playlist.json').read_text())
        entry = manifest['tracks'][0]
        for kind, response in [('audio', {'transcodedSha256': 'A'*43, 'transcodedInfo': {'format': 'mp3', 'duration': 12.5, 'fileSize': 1000}}), ('icon', {'displayIcon': {'mediaId': 'B'*43}})]:
            data = (kind + ' source').encode()
            (root/entry[kind]).write_bytes(data)
            media.record(root/entry[kind+'Receipt'], {'status': 'uploaded', 'sourceSha256': media.sha(data), 'response': response})
        return manifest

    def test_new_project_builds_from_only_its_own_assets_and_receipts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'story'; self.prepare(root)
            digest = media.build_project(root)
            raw = (root/'build/content.json').read_bytes(); payload = json.loads(raw)
            self.assertEqual(digest, media.sha(raw))
            self.assertNotIn('cardId', payload)
            self.assertEqual(payload['content']['chapters'][0]['tracks'][0]['trackUrl'], 'yoto:#'+'A'*43)

    def test_stale_uploaded_audio_cannot_enter_a_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'story'; manifest = self.prepare(root)
            (root/manifest['tracks'][0]['audio']).write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'Asset changed'):
                media.build_project(root)
            self.assertFalse((root/'build/content.json').exists())

    def test_missing_branch_target_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'story'; manifest = self.prepare(root)
            manifest['interactive'] = True
            manifest['tracks'][0]['events'] = {'onEnd': 'repeat', 'onLhb': 'missing', 'onRhb': '01'}
            (root/'playlist.json').write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, 'missing track'):
                media.build_project(root)

    def test_readback_cannot_hide_a_changed_button_outcome(self):
        expected = {'title': 'Story', 'content': {'chapters': [{'tracks': [{'events': {'onLhb': {'cmd': 'goto', 'params': {'trackKey': 'left'}}}}]}]}}
        actual = json.loads(json.dumps(expected)); actual['cardId'] = 'abc12'
        media.verify_card({'card': actual}, expected, 'abc12')
        actual['content']['chapters'][0]['tracks'][0]['events']['onLhb']['params']['trackKey'] = 'right'
        with self.assertRaises(ValueError):
            media.verify_card({'card': actual}, expected, 'abc12')


if __name__ == '__main__':
    unittest.main()
