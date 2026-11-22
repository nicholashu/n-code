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

Use the PR's intended audience when deciding which artifacts to upload. GitHub attachments on public repositories can be read without authentication. Keep local media outside the checkout.

Check `--help` for `--attach` in the shell holding the local files. GitHub requires push access to upload images and videos with the CLI. Use one `--attach` per vetted file.

- Include ready media when creating a PR or top-level comment with `gh pr create --attach <path>` or `gh pr comment <pr-url> --attach <path>`.
- Append to an existing PR description with `gh pr edit <pr-url> --attach <path>`. This preserves the current body. To place media within the description, fetch the latest body into a file, add local Markdown references, and pass the full file with `--body-file` and the media with `--attach`.
- Append to an existing top-level comment with `gh pr comment <pr-url> --edit-last --attach <path>` only after confirming that the intended permalink is the latest comment by the signed-in account and that account has no concurrent writers on the PR. This preserves the current comment text. For another comment, edit it by ID if you already have the approved asset URL. When a local upload is still required, use the exact comment's GitHub editor if authorized.

If the CLI lacks attachment support, use the GitHub editor for the intended description or comment when authorized and available. Otherwise report the missing attachment and keep media verification pending.

Put video asset URLs on their own lines for inline playback. After each attempt, read back the exact description or comment and confirm its original text and attribution are intact and the expected assets are present. A nonzero exit can leave some uploads published. Retry only the missing files.

Verify the links with the access intended for reviewers. For a private PR, use an authenticated read of the rendered body and download the assets with repository access. Compare downloads with the originals and play or decode video. Publish stable asset URLs and keep temporary signed URLs out of the handoff. If reviewers' access or playback cannot be verified, state the gap.

See [GitHub CLI attachment documentation](https://docs.github.com/en/github-cli/github-cli/attaching-files-with-github-cli) and the [PR comment command reference](https://cli.github.com/manual/gh_pr_comment).
