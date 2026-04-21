# Peplink Advisor

An AI assistant for Peplink hardware questions — spec lookups, side-by-side comparisons, and use-case-driven device recommendations grounded in a dataset of 103 current devices plus a curated solutions library.

This repo ships **two deployment targets from a single source of truth**:

- **Anthropic** — published in two Anthropic-native formats (both `.zip`; Claude Desktop's upload handler rejects any other extension):
  - `peplink-advisor-anthropic-plugin-<version>.zip` — plugin-bundle layout with `.claude-plugin/plugin.json` at the root. This is what Claude Desktop's Customize menu and Claude Code plugin installs accept.
  - `peplink-advisor-anthropic-standalone-<version>.zip` — single-skill layout (`peplink-advisor/SKILL.md` at the root) for dropping into `~/.claude/skills/`.
- **ChatGPT** (Custom GPT) — packaged as a knowledge bundle with pasted Instructions.

Both builds are produced from the same `core/` directory by the scripts in `build/`. CI runs on every push; GitHub Releases publish both artifacts on every tag.

## Layout

```
peplink-advisor/
├── core/                       # The portable 90% — shared by both adapters.
│   ├── SKILL.md                # Instructions for the model (body only, no frontmatter).
│   ├── scripts/
│   │   ├── query.py            # Helper the model runs to query the dataset.
│   │   └── enrich_datasheets.py# Maintenance script for datasheet URL discovery.
│   ├── data/
│   │   └── peplink_all_devices.json
│   ├── solutions/              # Curated deployment recipes (markdown + YAML frontmatter).
│   └── references/             # On-demand reference material.
├── adapters/
│   ├── anthropic/              # Plugin manifest + SKILL.md frontmatter.
│   └── chatgpt/                # Instructions template + knowledge manifest + deploy README.
├── build/
│   ├── common.py
│   ├── build_anthropic.py      # -> Desktop skill zip + Cowork/Code plugin bundle
│   └── build_chatgpt.py        # -> dist/peplink-advisor-chatgpt-<version>.zip
└── .github/workflows/
    ├── ci.yml                  # Build both adapters on every push/PR.
    └── release.yml             # Cut a GitHub Release on every `v*` tag.
```

## Install / deploy

### Claude Desktop (Customize menu)

Grab `peplink-advisor-anthropic-plugin-<version>.zip` from the latest [GitHub Release](../../releases). In Claude Desktop, go to Customize and upload the zip. Claude Desktop requires the `.zip` extension and a `.claude-plugin/plugin.json` at the zip root — this artifact has both.

### Claude Code plugins

Same zip — `peplink-advisor-anthropic-plugin-<version>.zip`. Use `/plugin install` or point `--plugin-dir` at the unpacked directory.

### Claude Code skills (standalone)

If you'd rather drop the skill into `~/.claude/skills/`, grab `peplink-advisor-anthropic-standalone-<version>.zip` and unzip it so the skill lives at `~/.claude/skills/peplink-advisor/SKILL.md`.

### ChatGPT Custom GPT

Grab `peplink-advisor-chatgpt-<version>.zip` from the latest [GitHub Release](../../releases), unzip it, and follow `README-deploy.md` inside.

## Customizing behavior

For account- or user-specific defaults, edit `core/SKILL.md` and add the rules under `## User-specific instructions`, below the line `User instructions should be inserted below this line.` Those instructions flow into both the Anthropic and ChatGPT builds automatically because `core/SKILL.md` is the shared source of truth.

## Develop

```bash
# Build both artifacts locally.
python3 build/build_anthropic.py
python3 build/verify_anthropic_artifacts.py
python3 build/build_chatgpt.py
python3 build/verify_chatgpt_bundle.py

# Sanity-check query.py against the dataset.
python3 core/scripts/query.py list
python3 core/scripts/query.py show "Balance 20X"
python3 core/scripts/query.py compare "HD2 MBX 5G" "HD4 MBX 5G"
```

## Release

1. Make your changes in `core/` (and adapters if needed).
2. Bump `version` in `adapters/anthropic/.claude-plugin/plugin.json`.
3. Update `CHANGELOG.md`.
4. Build and verify the release artifacts locally:
   ```bash
   python3 build/build_anthropic.py
   python3 build/verify_anthropic_artifacts.py
   python3 build/build_chatgpt.py
   python3 build/verify_chatgpt_bundle.py
   ```
5. Publish the release using either path:
   ```bash
   # Option A: tag push
   git add -A
   git commit -m "Release v0.2.0"
   git tag v0.2.0
   git push --follow-tags
   ```
   Or run **Actions -> Release -> Run workflow** on the commit you want to ship.
   The manual workflow defaults to creating/updating tag `v<plugin.json version>`
   for that commit; leave `publish_release` checked to publish the GitHub Release,
   or uncheck it for an artifact-only dry run.
6. GitHub Actions builds both artifacts and attaches them to the Release.

## Refreshing the dataset

See `CONTRIBUTING.md` for the full procedure, but the short version:

```bash
# Replace the JSON file with your new export, then re-probe datasheet URLs.
cp /path/to/new-peplink-export.json core/data/peplink_all_devices.json
python3 core/scripts/enrich_datasheets.py

# Update the "Dataset last updated" line in core/SKILL.md.
# Bump version, commit, tag, push.
```

## License

MIT. See `LICENSE`.

The `peplink_all_devices.json` dataset is derived from Peplink's publicly published specifications and is redistributed here for compatibility/fair-use purposes. Peplink's own site remains the authoritative source; verify any spec with the linked Datasheet URL before committing it to a customer quote.
