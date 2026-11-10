# Media commands

Run `python3 SKILL/scripts/yoto_media.py --help`, replacing `SKILL` with this
skill's resolved directory. Use Python 3 with Pillow and msgpack installed. Install Python dependencies with `python3 -m pip install -r SKILL/requirements.txt`
in the chosen environment. Audio checks require ffmpeg. The commands refuse existing
outputs. Keep outputs and private receipts in the story project.

## Drawings and covers

```sh
python3 "$SKILL/scripts/yoto_media.py" gif icons/talking.gif frames/01.png frames/02.png frames/03.png --durations 1200,160,1200
python3 "$SKILL/scripts/yoto_media.py" cover artwork/poster-master.png artwork/cover-upload.png
```

GIF input order is explicit. Each drawing must be 16x16. Transparent pixels
composite onto black for the player. The exporter uses one lossless palette,
refuses more than 256 shared colours, disables dithering, loops forever and
checks every decoded pixel and timing slot. It also saves an enlarged contact
sheet. Repeated holds may merge in the GIF without changing playback timing.

Cover accepts an existing illustrated master at least 600x825, preserves the
composition and pads to 600x825. It does not create an illustration or title.
Keep the high-resolution master and inspect the upload derivative.

## Fish API or local speech

```sh
python3 "$SKILL/scripts/yoto_media.py" speech scene.txt audio/scene.mp3 --voice VOICE_ID --model APPROVED_MODEL
python3 "$SKILL/scripts/yoto_media.py" speech scene.txt audio/scene.mp3 --voice LOCAL_REFERENCE_ID --local http://127.0.0.1:8080
```

API mode reads `FISH_API_KEY` privately from the environment. Choose the approved
model explicitly; there is no fallback. Local mode sends msgpack to an existing
Fish Speech `/v1/tts` server. Its loaded checkpoint selects the model. It sends
no cloud key and accepts loopback only; use an existing SSH tunnel for a remote
server. This command does not install models or start services. For another
local engine, render with its supported CLI and import the reviewed audio.

Both modes decode-check the returned MP3 and save text/audio hashes, voice and
provider mode beside it. One text file produces one clip. Split dialogue into
speaker clips, then concatenate them with ffmpeg in script order. Listen for clipped
endings, pronunciation, joins and voice consistency before upload. Failed API
requests do not auto-retry or silently spend again.

## Upload assets and publish a new playlist

Set `YOTO_ACCESS_TOKEN` through the available private credential mechanism.
Use an authorized token with content and media permissions. No existing app or
project login is required; a token is still required for account operations.

```sh
python3 "$SKILL/scripts/yoto_media.py" upload audio audio/scene.mp3 receipts/scene.json
python3 "$SKILL/scripts/yoto_media.py" upload icon icons/talking.gif receipts/talking.json
python3 "$SKILL/scripts/yoto_media.py" upload cover artwork/cover-upload.png receipts/cover.json
python3 "$SKILL/scripts/yoto_media.py" publish-new build/content.json card.json --sha256 REVIEWED_PAYLOAD_HASH
```

The `new` command creates the receipts directory. Audio upload requests a signed
upload URL, sends MP3 bytes without the account token to that URL and polls for
transcoding. Icon upload preserves animation with `autoConvert=false`. Cover
upload returns `response.coverImage.mediaUrl`. The project builder attaches that
URL to the playlist metadata. Receipts retain the full response and source SHA256.
See [the project format](project.md) to connect assets and receipts, then build
and review the final payload before publication.

Publication requires the compiled payload under `PROJECT/build/` and the canonical
`PROJECT/card.json` receipt, so choosing another receipt name cannot bypass a
pending create. Publication reserves `create_pending` before POST and never retries an uncertain
create. It saves the returned card ID before readback. Its final status means
chapter/track content, title and requested metadata passed readback. It explicitly
leaves downloaded asset bytes and hardware unverified. Reconcile pending receipts
manually against the Yoto library, rather than deleting them and retrying.
The bundled client only creates new playlists. Updating an existing playlist
needs a separately scoped owned-target update workflow.

API references checked 10 November 2026:
- [Fish hosted API](https://fish.audio/developers/)
- [Local Fish Speech inference](https://speech.fish.audio/inference/)
- [Yoto animated icons](https://yoto.dev/icons/uploading-animated-gifs/)
- [Yoto covers](https://yoto.dev/myo/uploading-cover-images/)
- [Yoto audio upload](https://yoto.dev/myo/uploading-to-cards/)
