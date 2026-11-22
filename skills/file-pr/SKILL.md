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

Use `gh` for local screenshots and videos. Keep the files outside the checkout
and check that they're suitable for the people who can see the PR. Anyone
with the URL can view attachments on a public repository.

Check `--help` for `--attach` in the shell where the files are. GitHub requires
push access for uploads. Pass one `--attach` per file. Use
`leaving-pr-comments` for attribution if you have it.

- When opening a PR or posting a top-level comment, use `--attach` for media
  that's ready. Pass prepared text with `--body-file`.
- To append media to a PR description, run
  `gh pr edit <pr-url> --attach <path>`. This keeps the existing text. To put
  media elsewhere in the description, fetch the latest text and add Markdown
  references to the local files. Pass the complete text with `--body-file` and
  the files with `--attach`.
- To append media to a posted top-level comment, use
  `gh pr comment <pr-url> --edit-last --attach <path>` only if its permalink
  matches the latest comment by the signed-in account and nobody else is
  writing to the PR with that account. For another comment, edit it by ID if
  you have the approved asset URL. If you still need to upload a file, use that
  comment's GitHub editor when authorized.

If `gh` lacks `--attach`, use the GitHub editor for the exact description or
comment when authorized. Report any required file you could not upload and
keep its verification pending.

Put each video URL on its own line for inline playback. After each attempt,
read back the exact description or comment. Check that the original text and
attribution are intact and that the expected media appears. The command may
add some media before it exits with an error. Retry only the missing files.

Check access using the same permissions as reviewers. For a private PR, use an
authenticated read of the rendered text, for example via GraphQL `bodyHTML`,
and download the files with repository access. For required evidence, compare the downloads with the originals and
play or decode each video. Put stable URLs in the handoff and keep temporary
signed URLs out of it. Report any required file you could not verify and keep
review pending.

See [GitHub CLI attachment documentation](https://docs.github.com/en/github-cli/github-cli/attaching-files-with-github-cli)
and the [PR comment command reference](https://cli.github.com/manual/gh_pr_comment).
