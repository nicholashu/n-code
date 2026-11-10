#!/usr/bin/env python3
"""Prepare Yoto media; network commands run only when explicitly selected."""
import argparse
import base64
import math
import time
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError('Redirect refused')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(path, data):
    # Exclusive creation protects reviewed assets and uncertain upload receipts.
    with Path(path).open('xb') as stream:
        stream.write(data)


def record(path, value):
    save(path, (json.dumps(value, indent=2) + '\n').encode())


def request(url, data, headers):
    with build_opener(NoRedirect()).open(Request(url, data=data, headers=headers), timeout=180) as response:
        return response.read()


def gif(frames, output, milliseconds):
    from PIL import Image
    if not frames or any(t < 20 or t % 10 for t in milliseconds) or len(frames) != len(milliseconds):
        raise ValueError('Supply one duration per frame, in 10 ms steps, at least 20 ms')
    images = []
    for path in frames:
        with Image.open(path) as im:
            if im.size != (16, 16) or getattr(im, 'n_frames', 1) != 1:
                raise ValueError('Each source must be one 16x16 frame')
            rgba = im.convert('RGBA')
            background = Image.new('RGBA', im.size, 'black')
            images.append(Image.alpha_composite(background, rgba).convert('RGB'))
    if len({im.tobytes() for im in images}) < 3:
        raise ValueError('Use at least three distinct drawings')
    colours = set().union(*(set(im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata()) for im in images))
    if len(colours) > 256:
        raise ValueError('Use at most 256 shared colours; refusing lossy quantization')
    palette = sorted(colours)
    palette_image = Image.new('P', (1, 1))
    palette_image.putpalette([c for rgb in palette for c in rgb] + [0] * (768 - len(palette) * 3))
    indexed = [im.quantize(palette=palette_image, dither=Image.Dither.NONE) for im in images]
    buffer = io.BytesIO()
    indexed[0].save(buffer, format='GIF', save_all=True, append_images=indexed[1:],
                    duration=milliseconds, loop=0, disposal=2, optimize=False)
    data = buffer.getvalue()
    with Image.open(io.BytesIO(data)) as decoded:
        actual = []
        for i in range(decoded.n_frames):
            decoded.seek(i)
            actual.extend([decoded.convert('RGB').tobytes()] * (decoded.info['duration'] // 10))
        expected = [im.tobytes() for im, t in zip(images, milliseconds) for _ in range(t // 10)]
        if actual != expected or decoded.info.get('loop') != 0:
            raise ValueError('Export changed pixels or timing')
    save(output, data)
    sheet = Image.new('RGB', (16 * len(images), 16))
    for i, im in enumerate(images):
        sheet.paste(im, (16 * i, 0))
    sheet.resize((sheet.width * 8, 128), Image.Resampling.NEAREST).save(str(output) + '.contact.png')


def cover(source, output):
    from PIL import Image, ImageOps
    with Image.open(source) as im:
        im = ImageOps.exif_transpose(im).convert('RGB')
        if im.width < 600 or im.height < 825:
            raise ValueError('Supply a poster master at least 600x825; refusing upscaling')
        # Preserve the whole composition; review any letterboxing before upload.
        result = ImageOps.pad(im, (600, 825), method=Image.Resampling.LANCZOS, color='black')
        buffer = io.BytesIO()
        result.save(buffer, format='PNG')
        save(output, buffer.getvalue())


def speech(args):
    text = args.text.read_text().strip()
    if not text:
        raise ValueError('Empty speech text')
    body = {'text': text, 'format': 'mp3', 'reference_id': args.voice, 'prosody': {'speed': 1.0}}
    headers = {'Content-Type': 'application/json'}
    if args.local:
        url = urlsplit(args.local)
        if url.scheme != 'http' or url.hostname not in ('localhost', '127.0.0.1', '::1') or url.username or url.password or url.query or url.fragment or url.path not in ('', '/'):
            raise ValueError('Local server must be a loopback HTTP origin; use an SSH tunnel for remote hosts')
        import msgpack
        data = msgpack.packb(body, use_bin_type=True)
        headers['Content-Type'] = 'application/msgpack'
        endpoint = args.local.rstrip('/') + '/v1/tts'
    else:
        if not args.model:
            raise ValueError('Choose the approved Fish model with --model')
        headers.update({'Authorization': 'Bearer ' + os.environ['FISH_API_KEY'], 'model': args.model})
        data = json.dumps(body).encode()
        endpoint = 'https://api.fish.audio/v1/tts'
    audio = request(endpoint, data, headers)
    with tempfile.TemporaryDirectory() as directory:
        raw = Path(directory) / 'speech.mp3'
        raw.write_bytes(audio)
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(raw), '-f', 'null', '-'], check=True)
    save(args.output, audio)
    record(str(args.output) + '.source.json', {'textSha256': sha(args.text.read_bytes()), 'audioSha256': sha(audio),
           'voice': args.voice, 'model': args.model if not args.local else 'server-selected', 'local': bool(args.local)})


API = 'https://api.yotoplay.com'


def request_json(url, *, token, body=None):
    headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json'}
    data = None
    if body is not None:
        headers['Content-Type'] = 'application/json'
        data = json.dumps(body).encode()
    result = json.loads(request(url, data, headers))
    if not isinstance(result, dict):
        raise ValueError('Expected a JSON object')
    return result


def upload_audio(path, token):
    data = path.read_bytes()
    digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b'=').decode()
    info = request_json(API + '/media/transcode/audio/uploadUrl?' + urlencode({'sha256': digest, 'filename': path.name}), token=token)['upload']
    if info.get('uploadUrl'):
        url = urlsplit(info['uploadUrl'])
        if url.scheme != 'https' or not url.hostname or not url.hostname.endswith('.amazonaws.com') or url.username or url.password:
            raise ValueError('Unexpected upload destination')
        with build_opener(NoRedirect()).open(Request(info['uploadUrl'], data=data, method='PUT', headers={'Content-Type': 'audio/mpeg'}), timeout=180):
            pass
    upload_id = info['uploadId']
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,150}', upload_id):
        raise ValueError('Invalid upload ID')
    for _ in range(60):
        media = request_json(API + '/media/upload/' + upload_id + '/transcoded?loudnorm=false', token=token).get('transcode', {})
        if media.get('transcodedSha256'):
            return media
        time.sleep(1)
    raise TimeoutError('Transcoding still pending')


def verify_card(actual, expected, card_id):
    card = actual.get('card', {})
    if card.get('cardId') != card_id:
        raise ValueError('Readback returned another card')
    def compare(got, wanted, field=''):
        if isinstance(wanted, dict):
            if not isinstance(got, dict):
                raise ValueError('Readback object missing')
            for key, value in wanted.items():
                compare(got.get(key), value, key)
        elif isinstance(wanted, list):
            if not isinstance(got, list) or len(got) != len(wanted):
                raise ValueError('Readback list differs')
            for left, right in zip(got, wanted):
                compare(left, right, field)
        elif field == 'duration':
            if type(got) not in (int, float) or not math.isfinite(got) or abs(got - wanted) > 1:
                raise ValueError('Readback duration differs')
        elif got != wanted:
            if field in ('trackUrl', 'icon16x16') and isinstance(wanted, str) and wanted.startswith('yoto:#') and isinstance(got, str):
                url = urlsplit(got)
                hosts = {'trackUrl': 'secure-media.yotoplay.com', 'icon16x16': 'card-content.yotoplay.com'}
                if url.scheme == 'https' and url.hostname == hosts[field] and not url.username and not url.password and url.fragment == 'sha256=' + wanted[6:]:
                    return
            raise ValueError('Readback differs: ' + field)
    compare(card, expected)


def new_project(root, title):
    if not 1 <= len(title.strip()) <= 140:
        raise ValueError('Title must contain 1 to 140 characters')
    root.mkdir()
    for folder in ('audio', 'icons', 'artwork', 'receipts', 'build'):
        (root / folder).mkdir()
    record(root / 'brief.json', {'title': title})
    record(root / 'playlist.json', {'title': title, 'description': '', 'interactive': False, 'tracks': [
        {'key': '01', 'title': 'Opening', 'audio': 'audio/opening.mp3', 'audioReceipt': 'receipts/opening.json',
         'icon': 'icons/opening.png', 'iconReceipt': 'receipts/opening-icon.json'}]})
    (root / 'STORY.md').write_text('# ' + title + '\n\nWrite the story here.\n')
    (root / '.gitignore').write_text('/audio/\n/receipts/\n/build/\n/card.json\n.env*\n')


def build_project(root):
    manifest = json.loads((root / 'playlist.json').read_text())
    title = manifest['title']
    if not isinstance(title, str) or not 1 <= len(title.strip()) <= 140:
        raise ValueError('Invalid title')
    entries = manifest['tracks']
    keys = [entry['key'] for entry in entries]
    if not 1 <= len(entries) <= 100 or len(set(keys)) != len(keys) or any(not isinstance(k, str) or not k or k == 'repeat' for k in keys):
        raise ValueError('Use 1 to 100 tracks with unique nonempty string keys')
    def receipt(entry, kind):
        source = (root / entry[kind]).read_bytes()
        item = json.loads((root / entry[kind + 'Receipt']).read_text())
        if item.get('status') != 'uploaded' or item.get('sourceSha256') != sha(source):
            raise ValueError('Asset changed or upload is incomplete')
        return item['response']
    tracks = []
    for entry in entries:
        audio = receipt(entry, 'audio')
        digest = audio['transcodedSha256']
        info = audio['transcodedInfo']
        icon = receipt(entry, 'icon')['displayIcon']['mediaId']
        if not re.fullmatch(r'[A-Za-z0-9_-]{43}', digest) or not re.fullmatch(r'[A-Za-z0-9_-]{43}', icon):
            raise ValueError('Invalid uploaded media hash')
        if info['format'] not in ('mp3', 'aac', 'alac', 'flac', 'pcm_s16le', 'opus', 'ogg', 'x-m4a', 'wav', 'aiff', 'mpeg') or type(info['duration']) not in (int, float) or not math.isfinite(info['duration']) or info['duration'] <= 0 or type(info['fileSize']) is not int or info['fileSize'] <= 0:
            raise ValueError('Invalid transcoded audio metadata')
        track = dict(key=entry['key'], uid=entry['key'], title=entry['title'], type='audio', trackUrl='yoto:#' + digest,
                     format=info['format'], duration=info['duration'], fileSize=info['fileSize'], display={'icon16x16': 'yoto:#' + icon})
        if manifest.get('interactive'):
            events = entry['events']
            if set(events) != {'onEnd', 'onLhb', 'onRhb'}:
                raise ValueError('Interactive tracks require end and both button events')
            track['events'] = {}
            for event, target in events.items():
                if target != 'repeat' and target not in keys:
                    raise ValueError('Event points to a missing track')
                track['events'][event] = {'cmd': 'repeat'} if target == 'repeat' else {'cmd': 'goto', 'params': {'chapterKey': '01', 'trackKey': target}}
        tracks.append(track)
    chapter = dict(key='01', title=title, defaultTrackDisplay='', defaultTrackAmbient='', display=tracks[0]['display'], tracks=tracks)
    content = {'playbackType': 'interactive' if manifest.get('interactive') else 'linear', 'chapters': [chapter],
               'config': {'onlineOnly': False, 'autoadvance': 'none' if manifest.get('interactive') else 'next'}}
    if manifest.get('interactive'):
        content['editSettings'] = {'interactiveContent': True, 'editKeys': False}
        content['config'].update(resumeTimeout=0, disableTrackNav=True, disableChapterNav=True)
    metadata = {'description': manifest.get('description', '')}
    if 'cover' in manifest:
        metadata['cover'] = {'imageL': receipt(manifest, 'cover')['coverImage']['mediaUrl']}
    payload = dict(title=title, metadata=metadata, content=content)
    data = (json.dumps(payload, indent=2) + '\n').encode()
    save(root / 'build/content.json', data)
    return sha(data)


def upload(args):
    data = args.source.read_bytes()
    token = os.environ['YOTO_ACCESS_TOKEN']
    if args.kind == 'audio':
        if args.source.suffix.lower() != '.mp3':
            raise ValueError('Audio upload expects MP3')
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(args.source), '-f', 'null', '-'], check=True)
        result = upload_audio(args.source, token)
    else:
        from PIL import Image
        with Image.open(io.BytesIO(data)) as im:
            im.load()
            if args.kind == 'icon':
                if im.size != (16, 16) or im.format not in ('PNG', 'GIF'):
                    raise ValueError('Icon must be a 16x16 PNG or GIF')
                mime = 'image/gif' if im.format == 'GIF' else 'image/png'
            else:
                if im.size != (600, 825) or im.format != 'PNG':
                    raise ValueError('Run cover first: expected a 600x825 PNG')
                mime = 'image/png'
        suffix = ('displayIcons/user/me/upload?' + urlencode({'autoConvert': 'false', 'filename': args.source.stem})
                  if args.kind == 'icon' else 'coverImage/user/me/upload?autoconvert=true&coverType=default')
        result = json.loads(request('https://api.yotoplay.com/media/' + suffix, data,
                            {'Authorization': 'Bearer ' + token, 'Content-Type': mime}))
        if args.kind == 'icon' and not re.fullmatch(r'[A-Za-z0-9_-]{43}', result.get('displayIcon', {}).get('mediaId', '')):
            raise ValueError('Missing valid icon mediaId')
        if args.kind == 'cover' and not result.get('coverImage', {}).get('mediaUrl', '').startswith('https://'):
            raise ValueError('Missing cover URL')
    return {'sourceSha256': sha(data), 'response': result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('new', help='Create a fresh independent story project')
    p.add_argument('project', type=Path); p.add_argument('--title', required=True)
    p = commands.add_parser('build', help='Compile playlist.json and source-checked upload receipts offline')
    p.add_argument('project', type=Path)
    p = commands.add_parser('gif', help='Lossless export from ordered 16x16 drawings')
    p.add_argument('output', type=Path)
    p.add_argument('frames', nargs='+', type=Path)
    p.add_argument('--durations', required=True, help='Comma-separated milliseconds, one per frame')
    p = commands.add_parser('cover', help='Prepare a reviewed poster master for Yoto')
    p.add_argument('source', type=Path); p.add_argument('output', type=Path)
    p = commands.add_parser('speech', help='Fish API or an existing local Fish Speech server')
    p.add_argument('text', type=Path); p.add_argument('output', type=Path)
    p.add_argument('--voice', required=True); p.add_argument('--model')
    p.add_argument('--local', help='Existing loopback Fish server origin; no API key sent')
    p = commands.add_parser('publish-new', help='Create a new playlist from a reviewed compiled payload; never update an existing card')
    p.add_argument('payload', type=Path); p.add_argument('receipt', type=Path)
    p.add_argument('--sha256', required=True, help='SHA256 of the reviewed payload bytes')
    p = commands.add_parser('upload', help='Upload one asset and save its response, without publishing a playlist')
    p.add_argument('kind', choices=['audio', 'icon', 'cover'])
    p.add_argument('source', type=Path); p.add_argument('receipt', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'new':
            new_project(args.project, args.title)
            print('Created ' + str(args.project))
            return 0
        if args.command == 'build':
            print('Payload SHA256: ' + build_project(args.project))
            return 0
        target = args.receipt if args.command in ('upload', 'publish-new') else args.output
        if target.exists():
            raise ValueError('Output already exists; choose a new path')
        if args.command == 'gif':
            gif(args.frames, args.output, [int(t) for t in args.durations.split(',')])
        elif args.command == 'cover':
            cover(args.source, args.output)
        elif args.command == 'speech':
            if Path(str(args.output) + '.source.json').exists():
                raise ValueError('Speech provenance already exists')
            speech(args)
        elif args.command == 'publish-new':
            project = args.payload.resolve().parent.parent
            if args.payload.resolve().name != 'content.json' or args.payload.resolve().parent.name != 'build' or args.receipt.resolve() != project / 'card.json':
                raise ValueError('Use PROJECT/build/content.json and PROJECT/card.json; receipt names cannot bypass pending creates')
            raw = args.payload.read_bytes()
            payload = json.loads(raw)
            if sha(raw) != args.sha256 or 'cardId' in payload or not payload.get('title') or not payload.get('content', {}).get('chapters'):
                raise ValueError('Expected a reviewed new-card payload with matching hash')
            access = os.environ['YOTO_ACCESS_TOKEN']
            receipt = {'owner': 'yoto_media', 'status': 'create_pending', 'payloadSha256': sha(raw), 'payload': str(args.payload.resolve())}
            record(args.receipt, receipt)
            result = request_json('https://api.yotoplay.com/content', token=access, body=payload)
            card_id = result.get('card', {}).get('cardId', '')
            if not re.fullmatch(r'[A-Za-z0-9]{5}', card_id):
                raise ValueError('Unexpected card ID; reconcile pending receipt')
            receipt.update(cardId=card_id, status='readback_pending')
            args.receipt.write_text(json.dumps(receipt, indent=2) + '\n')
            actual = request_json('https://api.yotoplay.com/card/' + card_id, token=access)
            verify_card(actual, payload, card_id)
            card = actual.get('card', {})
            if card.get('title') != payload['title'] or any(card.get('metadata', {}).get(k) != v for k, v in payload.get('metadata', {}).items()):
                raise ValueError('Title or metadata differs on readback')
            receipt.update(status='content_readback_passed', assetBytesVerified=False, hardwareTested=False)
            args.receipt.write_text(json.dumps(receipt, indent=2) + '\n')
        else:
            # Reserve before network IO: uncertain uploads remain visible and cannot auto-repeat.
            record(args.receipt, {'status': 'upload_pending', 'sourceSha256': sha(args.source.read_bytes())})
            result = upload(args)
            temporary = args.receipt.with_suffix(args.receipt.suffix + '.tmp')
            record(temporary, dict(result, status='uploaded'))
            temporary.replace(args.receipt)
        print('Saved ' + str(target))
    except Exception as error:
        # HTTP exceptions can contain signed URLs. Never echo request/response bodies or credentials.
        print('Failed (' + type(error).__name__ + '). Check inputs, dependencies and private credentials; retain pending receipts.', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
