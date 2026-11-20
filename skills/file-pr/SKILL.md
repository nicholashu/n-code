---
name: file-pr
description: File a concise GitHub pull request with evidence suited to the change. Use when asked to open a PR or update its description and evidence.
---

# File a pull request

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

Check `gh pr edit --help` for `--attach`. If available, use one flag per vetted file and pass the complete description with `--body-file` when changing it. Use a bare asset URL for an inline video. If the CLI lacks this option, use GitHub's attachment editor when authorized and available. Otherwise report the missing attachment and keep media verification pending.

Read the published description back. An upload command can fail after attaching some files, so check what GitHub accepted before retrying. Verify the links using the access intended for reviewers. For a private PR, use an authenticated read of the rendered body and download each attachment with repository access. Compare the downloaded files to the originals and play or decode video. Publish the stable asset links and keep temporary signed URLs out of the description. If reviewers' access or playback cannot be verified, state the gap.

See the [GitHub CLI manual](https://cli.github.com/manual/gh_pr_edit) and [GitHub's attachment guide](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/attaching-files).
