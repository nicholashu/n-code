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

Use the verified public name of the model that wrote the comment and the user's name or GitHub login. Use the harness name if the model name is unavailable. Keep the comment outside the note.

Use the note for top-level PR comments, inline review comments, replies, and written explanations before resolving or dismissing feedback. Omit it for PR descriptions and for text the user asks to post verbatim without attribution. When editing an existing comment, preserve its attribution.

Lead with the conclusion and cite the code, result, or reproduction that supports it. Distinguish observations from judgment. Check the Markdown, quoted text, and media for private details before posting.

Verify the comment or review permalink after posting. Resolve a review thread only after its reply is visible at that link.

## Add media to a comment

When `file-pr` is installed, read [Attach and verify media](../file-pr/SKILL.md#attach-and-verify-media) for the full workflow.

For a new top-level comment, pass local screenshots and videos with `gh pr comment <pr-url> --attach <path>`. To append media to a posted comment with `--edit-last`, first verify that the exact permalink is the latest comment by the signed-in account and that the account has no concurrent writers on the PR. For any other comment, edit the exact comment by ID if an approved asset URL is available. Use that comment's GitHub editor for a local upload when authorized.

After each attempt, read back the exact comment. Verify the existing text and attribution, and check which media landed. If the upload partially failed, retry only the missing files. [GitHub CLI attachment documentation](https://docs.github.com/en/github-cli/github-cli/attaching-files-with-github-cli)
