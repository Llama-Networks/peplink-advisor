# Anthropic adapter

Packages `core/` into both Anthropic-native distribution formats. Both are
`.zip` files, because Claude Desktop's upload handler rejects any other
extension (see anthropics/claude-code#40414 and #28337):

- A plugin-bundle zip with `.claude-plugin/plugin.json` at the root — for
  Claude Desktop's Customize menu and Claude Code plugin installs
- A single-skill zip for dropping into `~/.claude/skills/`

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

- `dist/peplink-advisor-anthropic-plugin-<version>.zip` with this layout:

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

**Claude Desktop (Customize menu):** Upload
`peplink-advisor-anthropic-plugin-<version>.zip`. Claude Desktop requires the
`.zip` extension and a `.claude-plugin/plugin.json` at the zip root — this
artifact has both.

**Claude Code plugins:** Same zip — `/plugin install` or `--plugin-dir` the
unpacked directory.

**Claude Code skills (standalone):** Unzip
`peplink-advisor-anthropic-<version>.zip` into `~/.claude/skills/` so the
skill lives at `~/.claude/skills/peplink-advisor/SKILL.md`.

## Why this adapter is tiny

Everything that actually does the work lives in `core/`. This directory only
exists to turn that content into the two Anthropic packaging formats. If you
add or change a solution file, `query.py`, or `SKILL.md` body, do it in
`core/` — not here.
