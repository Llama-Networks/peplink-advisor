# Anthropic adapter

Thin wrapper that packages `core/` as a Claude Code / Cowork plugin.

## Files

- `.claude-plugin/plugin.json` — plugin manifest (name, version, description, author, keywords). Version should match the git tag being released.
- `frontmatter.yaml` — the YAML block that gets prepended to `core/SKILL.md` in the built artifact. This is what Claude reads to decide when to auto-load the skill.

## Build

From the repo root:

```bash
python3 build/build_anthropic.py
```

Produces `dist/peplink-advisor-<version>.plugin` (a zip renamed). Drop it into Cowork or Claude Code to install.

## Why this adapter is tiny

Everything that actually does the work lives in `core/`. This directory only exists to turn that content into a format an Anthropic host will auto-discover. If you add or change a solution file, `query.py`, or `SKILL.md` body, do it in `core/` — not here.
