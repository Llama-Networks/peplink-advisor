# Peplink Advisor

An AI assistant for Peplink hardware questions — spec lookups, side-by-side comparisons, and use-case-driven device recommendations grounded in a dataset of 103 current devices plus a curated solutions library.

This repo ships **two deployment targets from a single source of truth**:

- **Anthropic** (Claude Code / Cowork plugin) — auto-discovered skill, progressive disclosure, Cowork artifacts.
- **ChatGPT** (Custom GPT) — same content, packaged as a knowledge bundle with pasted Instructions.

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
│   ├── build_anthropic.py      # -> dist/peplink-advisor-anthropic-<version>.plugin
│   └── build_chatgpt.py        # -> dist/peplink-advisor-chatgpt-<version>.zip
└── .github/workflows/
    ├── ci.yml                  # Build both adapters on every push/PR.
    └── release.yml             # Cut a GitHub Release on every `v*` tag.
```

## Install / deploy

### Claude Code or Cowork

Grab `peplink-advisor-anthropic-<version>.plugin` from the latest [GitHub Release](../../releases) and install it via your host's plugin flow. That's it.

### ChatGPT Custom GPT

Grab `peplink-advisor-chatgpt-<version>.zip` from the latest [GitHub Release](../../releases), unzip it, and follow `README-deploy.md` inside.

## Develop

```bash
# Build both artifacts locally.
python3 build/build_anthropic.py
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
   python3 build/build_chatgpt.py
   python3 build/verify_chatgpt_bundle.py
   ```
5. Commit, tag, and push:
   ```bash
   git add -A
   git commit -m "Release v0.2.0"
   git tag v0.2.0
   git push --follow-tags
   ```
6. GitHub Actions builds both artifacts and attaches them to a new Release.

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
