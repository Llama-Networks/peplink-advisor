# Solutions Library

Curated deployment recipes. Each file captures a recurring scenario (maritime, retail, first responder, etc.) and pins the devices, licenses, topology, and gotchas so the skill gives consistent answers instead of rolling the dice every time.

## How to add a solution

1. Copy `_template.md` to a new file named in kebab-case after the scenario (e.g., `ferry-passenger-wifi.md`).
2. Fill in the YAML frontmatter. Be generous with `use_cases` — Claude matches on these substrings when the user describes a deployment.
3. Write the narrative as if briefing a colleague. Cover: why this scenario needs something specific, which device is the default pick, when to step up or down, what licenses are required, what accessories are typically in the bill of materials, known pitfalls.
4. Set `last_reviewed` to today's date. Re-review any solution whose date is older than the dataset's "last updated" date in `../SKILL.md`.

## Frontmatter fields

- `name` — human-readable title.
- `slug` — kebab-case identifier (match the filename).
- `use_cases` — list of substrings to match user scenarios. Lean into natural phrasing ("fishing charter", "food truck", "ambulance"), not jargon.
- `primary_devices` — product names exactly as they appear in the dataset (`query.py list` will confirm).
- `alternate_devices` — optional. Step-up or step-down picks.
- `licenses` — what the recommendation assumes the customer will buy.
- `last_reviewed` — ISO date. Used to flag stale recommendations.

Anything else belongs in the narrative body, not the frontmatter.
