# Independent story projects

The bundled CLI owns the whole path from a new directory to a new playlist.
It never imports another story project. Set `SKILL` to this skill's resolved path.

```sh
python3 "$SKILL/scripts/yoto_media.py" new woodland --title "The woodland bell"
cd woodland
# After authoring, rendering and uploading the assets:
python3 "$SKILL/scripts/yoto_media.py" build .
```

After `new`, write the actual story in `STORY.md`, render audio and artwork,
upload them with the media commands, then edit `playlist.json`. The scaffold
contains one opening track with paths for its audio, icon and receipts. Each
track has these fields:

```json
{
  "key": "opening",
  "title": "The woodland bell",
  "audio": "audio/opening.mp3",
  "audioReceipt": "receipts/opening.json",
  "icon": "icons/opening.gif",
  "iconReceipt": "receipts/opening-icon.json"
}
```

The root object contains `title`, `description`, `interactive` and `tracks`.
Paths resolve against the project directory. Track order is playback order for
a linear playlist. Keys must be unique. Add `cover` and `coverReceipt` at the
root to attach the reviewed cover using its upload receipt. The builder verifies
that local bytes still match the successful upload receipts. Changing an asset
requires uploading it again and reviewing its association.

For branching stories, set `interactive` to true. Each track must supply all
three events. Values are another track key or `repeat`:

```json
"events": {
  "onEnd": "choose-path",
  "onLhb": "repeat",
  "onRhb": "repeat"
}
```

Use separate spoken and silent decision tracks. The spoken prompt ends by
jumping to its decision track. That track repeats silence on `onEnd` and sends
left and right presses to the two outcome keys. Generate a true silent MP3:

```sh
ffmpeg -v error -f lavfi -i anullsrc=r=44100:cl=mono -t 120 -codec:a libmp3lame -b:a 128k audio/waiting.mp3
```

Upload it once and reuse its path and receipt for decision tracks. Their icons
show the ordered choices. Endings can jump to a replay prompt, then a silent
track whose two buttons return to the opening. `repeat` is reserved for the
repeat command; use another word for a track key. The compiler checks targets;
review reachability, endings and spoken continuity yourself.

Build writes `build/content.json` exclusively and prints its SHA256. Keep a
reviewed build before deliberately removing it to rebuild. Publication takes
that exact hash and uses the project's canonical `card.json` receipt. Creation,
readback and hardware verification remain separate stages. No existing card ID
is needed or accepted for creation.
