---
name: leaving-pr-comments
description: Write or edit GitHub PR comments, including inline review replies and adding screenshots or video to an existing comment. Use for comment attribution, posting, and read-back.
---

# Leave PR comments

Start a new agent-authored comment posted on the user's behalf with a GitHub note.

```md
> [!NOTE]
> 🤖 **<model> responding on behalf of <user>**

Comment text goes here.
```

Use the verified public name of the model that wrote the comment and the user's
name or GitHub login. Use the harness name if the model name is unavailable.
Keep one attribution in the note and place the reply outside it.

Use the note for top-level PR comments, inline review comments, replies, and
written explanations before resolving or dismissing feedback. Omit it for PR
descriptions, commit messages, and text the user asks to post verbatim without
attribution. Preserve attribution when editing an existing comment.

Lead with the conclusion and cite the code, result, or reproduction that
supports it. Distinguish observations from judgment. Preview the Markdown and
check it, quoted text, and media for secrets and private details before posting.

Verify the comment or review permalink after posting. Resolve a review thread
only after you confirm the intended reply is visible there.

## Add media to a comment

When `file-pr` is installed, read [the media workflow](../file-pr/SKILL.md#attach-and-verify-media).

If only this skill is installed, use the following steps. For a new
top-level comment, use `gh pr comment <pr-url> --attach <path>` with
the prepared body. For a posted comment, use `--edit-last --attach` only if
the exact permalink is the latest by the signed-in account and there are no
concurrent writers using that account on the PR. For other comments, edit the
exact comment by ID if you have the approved asset URL. Use that comment's
GitHub editor for a local upload when authorized.

Read back the exact comment after each attempt. Verify its text, attribution,
and attachments. Retry only the files that are still missing.
