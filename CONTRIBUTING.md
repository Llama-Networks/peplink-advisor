# Contributing to Peplink Advisor

Peplink Advisor is meant to help people specify Peplink solutions with clear source grounding. Contributions are most useful when they improve accuracy, add practical deployment knowledge, or make the packaged assistant easier to use.

## Useful Contributions

- Correct a spec, SKU, add-on, URL, or licensing note.
- Add a missing current device, module, accessory, or SKU mapping.
- Improve a deployment recipe for a real-world use case.
- Add a new solution recipe for a common scenario.
- Report a confusing answer pattern or missing caveat in the assistant instructions.
- Report packaging or installation problems with a release download.

Please do not add confidential customer details, private price lists, distributor-only terms, or unsourced commercial claims.

## Source Standard

For catalog and spec changes, include enough information for another person to verify the update:

- Product name or exact SKU.
- Field being corrected or added.
- Current value in this repository, if present.
- Proposed value.
- Official Peplink product page, datasheet, or other public source URL.
- Date you checked the source.

Preserve Peplink wording for licensing and hardware revision caveats when that wording affects whether a feature is standard, included with PrimeCare, firmware-gated, SKU-specific, or separately licensed.

## Catalog Changes

Catalog data lives in `core/data/peplink_all_devices.json`.

If you propose a data update, prefer a complete corrected record or export over a vague description. At minimum, provide the exact fields and source links needed to make the correction.

When checking the local catalog, use:

```bash
python3 core/scripts/query.py show "B One 5G"
python3 core/scripts/query.py skus "B One 5G"
python3 core/scripts/query.py skus --find "LIC-VWAN" --type router
```

The query helper keeps reviews focused on the relevant device or SKU instead of requiring people to inspect the full JSON file manually.

## Solution Recipes

Solution recipes live in `core/solutions/`. They are for repeatable deployment patterns, not one-off guesses.

A useful recipe should include:

- The deployment scenario and assumptions.
- Primary device recommendations.
- Reasonable alternatives and when to choose them.
- Required or optional licenses.
- Common accessories or modules.
- Material caveats, especially throughput, environment, power, antenna, SIM, and PrimeCare dependencies.
- Source checks against the dataset using `core/scripts/query.py`.

Do not recommend legacy or end-of-sale hardware for new solutions. Retain it for existing-installation support, comparisons, and migration. Check exact hardware revisions and SKU variants with `query.py ... --new-solutions`; a warning alone does not make a legacy product eligible. Preserve lifecycle evidence and reviewed SKU mappings when refreshing source workbooks.

## Assistant Behavior

Assistant instructions live in `core/SKILL.md`. Changes there affect how the packaged assistant answers.

Good behavior changes usually make the assistant:

- Ask for missing deployment constraints before recommending hardware.
- Cite datasheet and product URLs when giving concrete specs.
- Preserve licensing notes and SKU-specific caveats.
- Say when the dataset does not contain an answer.
- Avoid over-recommending add-ons when the user's scenario does not require them.

## Local Validation

If you are editing files locally, these checks are useful before sharing a change:

```bash
python3 -m py_compile core/scripts/query.py
python3 core/scripts/query.py show "B One 5G"
python3 core/scripts/query.py skus "B One 5G"
python3 core/scripts/query.py search "GPS"
python3 -m unittest discover -s core/scripts -p 'test_*.py'
```

If you changed packaged instructions or adapter files, rebuilding the release packages is also useful:

```bash
python3 build/build_anthropic.py
python3 build/verify_anthropic_artifacts.py
python3 build/build_chatgpt.py
python3 build/verify_chatgpt_bundle.py
```

## Publishing a Release

The version in `adapters/anthropic/.claude-plugin/plugin.json` controls all three download filenames and the packaged Claude plugin version. Running the Release workflow does not automatically increment it.

1. Update that version to the next unused release number and move the relevant `CHANGELOG.md` entries from `Unreleased` to a dated version heading.
2. Run the local checks above and `python3 -m unittest discover -s build -p 'test_*.py'`, then commit and push the changes through the repository's normal review process. Wait for CI to pass.
3. In GitHub, open **Actions → Release → Run workflow**, select the branch containing the version update, leave **publish_release** checked, and leave **tag_name** blank. The workflow creates `v<plugin.json version>` at that run's commit and publishes all three packages. An explicit tag must match that version exactly.

Alternatively, push a matching tag at the version-update commit to trigger the same workflow. For example, after updating the manifest to `0.2.4`:

```bash
git tag v0.2.4
git push origin v0.2.4
```

Creating a release only through GitHub's Releases page does not trigger the package build. Use the Release workflow or a tag push so the downloads are attached automatically.

To build without publishing, uncheck **publish_release** in the manual workflow form; the packages are available in that run's **Artifacts** section. A publishing run may reuse an existing tag only when it points to the exact commit being built. If the tag points to older code, increment the manifest version and publish a new tag.

## Where Files Live

| Change | Location |
| --- | --- |
| Device specs, SKUs, add-ons, and source URLs | `core/data/peplink_all_devices.json` |
| Deployment recipes | `core/solutions/` |
| Reference notes | `core/references/` |
| Assistant behavior | `core/SKILL.md` |
| Catalog query helper | `core/scripts/query.py` |
| Claude packaging metadata | `adapters/anthropic/` |
| ChatGPT package instructions and config | `adapters/chatgpt/` |

Keep changes focused. A spec correction, a solution recipe, and a behavior rewrite are easier to review as separate changes.
