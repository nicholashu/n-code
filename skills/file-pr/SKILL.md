---
name: file-pr
description: File a concise GitHub pull request with evidence suited to the change. Use when asked to open a PR, edit its description, or attach media to a PR comment.
---

# File a pull request

To add media to an existing PR description or comment, go to [Attach and verify media](#attach-and-verify-media).

## Choose the base

Check for an existing PR for the head branch. Use the base required by the task and repository. A stacked PR targets its immediate dependency. Review the diff against the actual base before publishing.

Write a title that follows the repository's conventions and names the change. Start the description with the problem and what now happens. Add the evidence reviewers need to check the change and note any limits. Use the repository's template and include authorship credit when required.

Before publishing, check the title, description, and attachments for secrets, personal data, and internal details. Follow the draft and review requirements. Confirm the published URL, base, head, and draft state. Report any preview that publication triggered.

If T3 Code offers PR linking for the current thread, link the PR and read the link back. Use the repository's approval process for merges and releases. If asked to monitor CI and reviews, use `babysit-pr` when installed.

## Choose evidence

- **UI changes.** Link screenshots and a short recording of the affected flow. Show before and after when reviewers need to compare them.
- **API changes.** Show a sanitized request and observed result, or a focused contract or integration check. Include fallback or failure evidence when it changed.
- **Mixed changes.** Cover the UI and API behaviors that changed. Use a small diagram if routing is hard to follow. Use a graph when measured results support a comparison, with units, conditions, and limitations labeled.

## Attach and verify media

Use `gh` for local screenshots and videos. Keep media outside the checkout
and vet it for the intended audience. Anyone with the URL can view attachments
on a public repository. Check `--help` for `--attach` in the shell holding the
files. GitHub requires push access to upload media. Use one flag per file. For comment attribution, apply
`leaving-pr-comments` when installed.

- Include ready media with `--attach` when creating a PR or a top-level
  comment. Use `--body-file` for prepared text.
- Append to an existing PR description with
  `gh pr edit <pr-url> --attach <path>`. This preserves the current body. To
  place media within it, fetch the latest body, add local Markdown references,
  and provide the full file with `--body-file` and the media with `--attach`.
- Append to an existing top-level comment with
  `gh pr comment <pr-url> --edit-last --attach <path>` only when the target
  permalink is the latest comment by the signed-in account and that account has
  no concurrent writers on the PR. This preserves the current body. For other
  comments, edit the exact comment by ID if you have the approved asset URL.
  Use that comment's GitHub editor for local uploads when authorized.

If the CLI lacks attachment support, use the GitHub editor for the exact
description or comment when authorized. Report any required upload you could
not complete and keep its verification pending.

Put video asset URLs on their own lines for inline playback. After each
attempt, read back the exact description or comment and check that the original
text, attribution, and expected media are intact. A nonzero exit can leave
some uploads published. Retry only the missing files.

Verify the media with the access intended for reviewers. For a private PR,
read the rendered body with authentication, for example via GraphQL
`bodyHTML`, and download with repository access. For required review evidence,
compare downloads with the originals and play or decode any video. Use stable
asset URLs and keep temporary signed URLs out of the handoff. Report any
required asset you could not verify and keep review pending.

See [GitHub CLI attachment documentation](https://docs.github.com/en/github-cli/github-cli/attaching-files-with-github-cli)
and the [PR comment command reference](https://cli.github.com/manual/gh_pr_comment).
