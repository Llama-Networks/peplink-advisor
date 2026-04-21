# Anthropic adapter

Packages `core/` into both Anthropic-native distribution formats:

- A Claude Desktop / claude.ai skill zip for "Upload skill"
- A Claude Cowork / Claude Code plugin bundle for hosts that expect
  `.claude-plugin/plugin.json`

## Files

- `frontmatter.yaml` — the YAML block that gets prepended to `core/SKILL.md` in
  both built artifacts. Must define `name` (lowercase letters/numbers/hyphens
  only, matching the top-level desktop skill folder and the plugin skill
  directory) and `description`.
- `.claude-plugin/plugin.json` — the plugin manifest. It remains the single
  source of truth for the version string read by `build/common.py`, and it is
  shipped in the Cowork / Claude Code plugin artifact.

## Build

From the repo root:

```bash
python3 build/build_anthropic.py
```

Produces:

- `dist/peplink-advisor-anthropic-<version>.zip` with this layout:

  ```
  peplink-advisor/
  ├── SKILL.md
  ├── scripts/
  ├── data/
  ├── solutions/
  └── references/
  ```

- `dist/peplink-advisor-anthropic-plugin-<version>.plugin` with this layout:

  ```
  .claude-plugin/
  └── plugin.json
  skills/
  └── peplink-advisor/
      ├── SKILL.md
      ├── scripts/
      ├── data/
      ├── solutions/
      └── references/
  ```

## Install

**Claude Desktop / claude.ai:** Customize → Skills → Upload skill, then pick
`peplink-advisor-anthropic-<version>.zip`.

**Claude Code skills:** Unzip `peplink-advisor-anthropic-<version>.zip` into
`~/.claude/skills/` so the skill lives at
`~/.claude/skills/peplink-advisor/SKILL.md`.

**Claude Cowork / Claude Code plugins:** Use
`peplink-advisor-anthropic-plugin-<version>.plugin` when the host expects a
plugin bundle with `.claude-plugin/plugin.json`.

## Why this adapter is tiny

Everything that actually does the work lives in `core/`. This directory only
exists to turn that content into the two Anthropic packaging formats. If you
add or change a solution file, `query.py`, or `SKILL.md` body, do it in
`core/` — not here.
