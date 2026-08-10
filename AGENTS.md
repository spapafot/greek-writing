# AGENTS.md

Instructions for coding agents that maintain this repository.

## Repository contents

Greek Writing is a portable agent skill written in Markdown. It has no build step and must not depend on a specific model or agent harness.

- `SKILL.md` is the source of truth for behavior.
- `README.md` explains installation, usage, patterns, and releases.
- `agents/openai.yaml` contains UI metadata only.
- The files in `.claude-plugin` support optional installation as a Claude Code plugin.
- `scripts/validate-package.py` checks the package's shared conventions.

## Maintenance conventions

- Keep `SKILL.md` under 500 lines and encoded as valid UTF-8.
- Use only `name` and `description` in the frontmatter.
- Keep the 37 patterns contiguous. Each pattern must contain exactly one `Πριν` and `Μετά` pair with an original Greek example. Keep every change synchronized with the table in `README.md`.
- Do not copy text or examples from the upstream Humanizer. Preserve the inspiration credit and repository link in `README.md`.
- Do not change factual details in examples merely to make a rewrite more vivid.
- When changing the version, update `plugin.json` and the release history in `README.md` together.
- Keep the documentation portable. References to Codex or Claude are examples of supported environments, not limitations.

## Pre-publication checks

    python scripts/validate-package.py
    npx skills add . --list
    claude plugin validate .
