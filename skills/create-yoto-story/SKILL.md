---
name: create-yoto-story
description: Create interactive Yoto stories, prepare GIFs, covers and Fish or local speech, and upload reviewed assets or playlists. Use when making or revising a Yoto story card.
---

# Create a Yoto story

This skill contains its own project builder and Yoto upload client. It needs no
previous story, card, repository or project-specific workflow. Use Python 3 with
Pillow and msgpack, plus ffmpeg for audio checks. Keep each story's sources,
media and receipts in a fresh project directory in the user's workspace.

## Write the story

Ask only for missing creative direction: theme and ideas, listener and age,
tone, approximate length and things to avoid. If asked to choose, choose and proceed.
Record the brief in `brief.json`. Offer a short premise before a long script
when the direction still needs discussion.

Create a fresh project with the bundled CLI's `new PROJECT --title TITLE`.
Write `STORY.md` and author `playlist.json` using [the project format](references/project.md).
Keep dialogue, pictures and branch outcomes consistent. Speak both options in
left/right order, then a clear ready cue. Use the silent waiting track for
unlimited thinking time. Review every route before producing audio. Spoken duration excludes waiting.
The builder accepts at most 100 tracks; combine stories in their intended order
and author menu jumps in the same project when a collection is requested.

## Produce media

Use [the media commands](references/media.md). They export drawings and poster
masters, synthesize speech and upload assets. They do not invent character art.
Use the image-generation skill for a new illustrated poster, or draw pixel frames
in a project-local Pillow script. Inspect real character references first.

Spoken scenes use character-focused 16x16 GIFs with several distinct drawings.
Keep the body and camera stable; animate readable eyes, mouths or actions.
Avoid two-frame flipping and whole-body wobble. Menus use static 16x16 PNGs.
Review the exact GIF at native size and enlarged, including the loop join and
contact sheet. The exporter proves pixels and timing, not likeness or good motion.
Keep the poster master separate from its upload derivative and any print sticker.

Choose voices and audition before a full render when voice fit is unresolved.
Use the approved Fish model, an existing local Fish Speech server, or reviewed
recordings. Local voice IDs belong to that server; cloud IDs are not interchangeable.
Use natural speech speed. Improve the script to change its length; do not stretch
speech or add padding. Listen to every final clip and decode-check it.

## Build and upload

Keep generation, asset upload, playlist publication, physical MYO linking and
player control separate. Follow the delivery stage the user requested. A draft
request does not authorize paid generation or publication. Finish an already
authorized stage without asking again.

Upload commands preserve responses and source hashes. The bundled `build PROJECT`
checks each receipt against its local asset and compiles `build/content.json`.
It rejects stale assets, duplicate track keys and missing branch targets. Review
branches, endings, icon mapping, duration and the printed payload hash.

`publish-new` creates a new playlist from those reviewed bytes. It refuses
`cardId` and existing canonical `card.json` receipts. An uncertain create leaves
a pending receipt; reconcile the library before another attempt. Existing-card
updates are outside this command's scope. The scripts never link a physical card
or control a player.

Report the title, project path and actual stage reached. Content readback, downloaded
asset verification and hardware/offline playback are separate claims. Preserve
sources and partial receipts; state any missing credentials or unverified stage.
