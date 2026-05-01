# Contributing to Peplink Advisor

Most changes happen in `core/`. The adapters are intentionally thin wrappers, don't add behavior there.

## Where does my change go?

| Change | Location |
| --- | --- |
| Updated device specs / new devices | `core/data/peplink_all_devices.json` (full export, not a patch) |
| New deployment recipe | `core/solutions/<slug>.md` (use `_template.md`) |
| New family reference | `core/references/<topic>.md` |
| Tweaking how the model answers | `core/SKILL.md` |
| New `query.py` subcommand | `core/scripts/query.py` |
| Plugin manifest / discovery string | `adapters/anthropic/` |
| ChatGPT GPT configuration / deploy instructions | `adapters/chatgpt/` |
| Build pipeline | `build/` |

## Authoring a new solution

1. Copy `core/solutions/_template.md` to `core/solutions/<slug>.md`.
2. Fill in the frontmatter first (`name`, `slug`, `use_cases`, `primary_devices`, `alternate_devices`, `licenses`, `last_reviewed`).
3. Write the body. Ground every concrete number against the dataset:
   ```bash
   python3 core/scripts/query.py show "Balance 20X"
   ```
4. Prefer the `Datasheet URL` over the `Product URL` when citing specs.
5. If your scenario stretches the "device recommendations" shape (e.g., a topology guide, a troubleshooting runbook), talk through the fit before adding it — solutions work best when they're recommendation-shaped.

## Refreshing the dataset

When you have updated JSON data:

```bash
# 1. Replace the file.
cp /path/to/peplink_all_devices.json core/data/peplink_all_devices.json

# 2. Re-probe datasheet URLs (adds/updates `Datasheet URL` in each device's metadata).
python3 core/scripts/enrich_datasheets.py

# 3. Update the "Dataset last updated: YYYY-MM-DD" line in core/SKILL.md.

# 4. Bump version in adapters/anthropic/.claude-plugin/plugin.json.

# 5. Update CHANGELOG.md.

# 6. Run the builds locally to confirm nothing broke:
python3 build/build_anthropic.py
python3 build/build_chatgpt.py
python3 build/verify_chatgpt_bundle.py
```

If the JSON schema changed (new nested sections, renamed fields), update the "Data shape quick reference" section in `core/SKILL.md` and run the query.py sanity checks from `.github/workflows/ci.yml` before merging.

## Versioning

`adapters/anthropic/.claude-plugin/plugin.json` is the single source of truth for version. Both build scripts read it; don't duplicate it elsewhere.

- **PATCH** (0.1.x) — dataset refresh, new solution, copy edits to SKILL.md.
- **MINOR** (0.x.0) — new query.py subcommand, breaking change to a solution's frontmatter schema, dataset schema change.
- **MAJOR** (x.0.0) — incompatible adapter changes (new plugin format, new GPT config shape).

## Releasing

See `README.md` for the tag-and-push workflow. CI must pass before tagging.

## Local iteration tip

While editing `core/SKILL.md`, symlink the built plugin into your Cowork or Claude Code plugins directory once, then keep re-running `build/build_anthropic.py` to overwrite the artifact in place. Restarting the host picks up the new version.
