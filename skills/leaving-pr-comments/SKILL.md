---
name: leaving-pr-comments
description: Write or edit GitHub PR comments, including inline review replies and adding screenshots or video to an existing comment. Use for comment attribution, posting, and read-back.
---

# Leave PR comments

Start each new comment you write on the user's behalf with this GitHub note.

```md
> [!NOTE]
> 🤖 **<model> responding on behalf of <user>**

Comment text goes here.
```

Use the verified public model name and the user's name or GitHub login. If the
model name is unavailable, use the name of the tool running the model. Put the
reply below the note and use a single attribution.

Use the note for PR comments, inline replies, and explanations before resolving
or dismissing feedback. Skip it for PR descriptions, commit messages, and any
text the user asks you to post verbatim without attribution. Preserve the
existing attribution when editing a comment.

Lead with the conclusion. Cite the code, result, or reproduction that supports
it, and make clear which points are your judgment. Preview the Markdown and
check the text, quotes, and media for secrets or private details before posting.

Read the saved reply and verify its permalink. Resolve the review thread
after you confirm the reply appears there.

## Add media to a comment

If you have `file-pr`, use [its media instructions](../file-pr/SKILL.md#attach-and-verify-media).

Otherwise, use `gh pr comment <pr-url> --attach <path>` with the prepared text
for a new top-level comment. For a posted top-level comment, use
`--edit-last --attach` only if its permalink matches the signed-in account's latest comment and
nobody else is writing to the PR with that account. Edit any other comment by
ID if you have the approved asset URL. If you still need to upload a file, use
that comment's GitHub editor when authorized.

After each attempt, read back the exact comment. Check its text, attribution,
and media. Retry only the missing files.
