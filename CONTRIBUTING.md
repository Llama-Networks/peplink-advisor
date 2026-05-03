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

Avoid recommending end-of-sale hardware unless the scenario explicitly requires it and the warning is clear.

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
```

If you changed packaged instructions or adapter files, rebuilding the release packages is also useful:

```bash
python3 build/build_anthropic.py
python3 build/build_chatgpt.py
python3 build/verify_chatgpt_bundle.py
```

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
