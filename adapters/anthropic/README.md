# Anthropic adapter

Packages `core/` as a Claude skill in the format Claude Desktop (and claude.ai)
expects for "Upload skill" — a zip whose root is a single folder named after
the skill, with `SKILL.md` at the top of that folder. This follows the
[Agent Skills open standard](https://agentskills.io) and the upload requirements
documented at
[How to create custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills).

## Files

- `frontmatter.yaml` — the YAML block that gets prepended to `core/SKILL.md` in
  the built artifact. Must define `name` (lowercase letters/numbers/hyphens
  only, matching the top-level folder in the zip) and `description` (what the
  skill does and when to use it — Claude reads this to decide when to load
  the skill).
- `.claude-plugin/plugin.json` — retained only as the single source of truth
  for the version string read by `build/common.py`. It is **not** shipped in
  the uploaded skill artifact; Claude Desktop skills don't use plugin.json.

## Build

From the repo root:

```bash
python3 build/build_anthropic.py
```

Produces `dist/peplink-advisor-anthropic-<version>.zip` with this layout:

```
peplink-advisor/
├── SKILL.md
├── scripts/
├── data/
├── solutions/
└── references/
```

## Install

**Claude Desktop / claude.ai:** Customize → Skills → Upload skill, then pick
the `.zip` file. The app validates the layout and `SKILL.md` frontmatter on
upload.

**Claude Code:** Unzip into `~/.claude/skills/` so the skill lives at
`~/.claude/skills/peplink-advisor/SKILL.md`. Claude Code watches that
directory and discovers the skill automatically — no plugin install step
required.

## Why this adapter is tiny

Everything that actually does the work lives in `core/`. This directory only
exists to turn that content into a Claude Desktop-compliant skill zip. If you
add or change a solution file, `query.py`, or `SKILL.md` body, do it in
`core/` — not here.
