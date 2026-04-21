# Peplink Advisor

This skill equips you to answer Peplink hardware questions accurately. The ground truth for all 103 current devices lives in `data/peplink_all_devices.json`. That file is ~1 MB; do **not** read it whole into context. Instead, run the `scripts/query.py` helper and reason over the small JSON slices it returns.

**Dataset last updated: 2026-04-17.** If the user asks about a device missing from the dataset, say so plainly rather than guessing — Peplink releases hardware frequently.

## When to use this skill

Trigger on any of:

- A Peplink product name or family (BR1, BR2, HD2, HD4, MBX, Balance, Transit, Dome, SDX, EPX, MAX, UBR, B One, AP One, AP Pro, SD Switch).
- Peplink-specific technology or licenses (SpeedFusion, PepVPN, InControl, PrimeCare, Hot Failover, FusionSIM, RemoteSIM, Drop-In Mode, SpeedFusion Connect, Synergy Mode).
- A deployment description where Peplink is plausibly the answer (bonded cellular, WAN aggregation, failover at a remote branch, maritime/vessel connectivity, transit/vehicle, first responder, broadcast/ENG, IoT gateway, retail with cellular backup).
- Direct requests to compare two or more networking devices if at least one is Peplink.

Don't trigger on generic "what router should I buy" questions that don't mention Peplink or a Peplink-shaped use case — defer to a broader answer.

## How to answer (by shape of question)

Pick the approach that fits the question, then ground every concrete number in `query.py` output.

### 1. Spec lookup ("Does the BR1 Pro 5G support GPS?")

Run `python3 scripts/query.py show "<device name>"` and read the specific field. If the user's question touches on a feature that often has licensing strings attached (SpeedFusion, Virtual WAN, x.509, eSIM), **include the `note` alongside the `value`** — the caveat is the answer, not optional flavor.

### 2. Side-by-side comparison ("Compare HD2 MBX vs HD4 MBX")

Run `python3 scripts/query.py compare "<name1>" "<name2>" [--sections Performance,Interfaces,...]`. For most comparison questions, limit sections to the ones the user cares about; dumping all nine sections is noisy.

When a device lacks a section another has (e.g., a switch vs a router), the cell comes back as `null` — say "not applicable" rather than inventing a value.

### 3. Feature filter ("Which Peplink routers support 5G?")

Use `filter`: `python3 scripts/query.py filter --type router --field "5G support" --value Yes`. The `--field` argument is a regex and `--value` is a case-insensitive substring. For broad questions ("anything that supports bonded cellular") fall back to `search`.

### 4. Free-text search ("Which devices mention dead reckoning?")

`python3 scripts/query.py search "<query>"` scans names, metadata, section/field names, values, and notes. Use it when you don't know which field to target.

### 5. Use-case → device recommendation ("We need connectivity for a fishing charter with two crew and guests")

This is the highest-value path and needs a deliberate approach:

1. **Check the solutions library first.** `ls solutions/` and skim any filenames that look related. If one matches, open it and use it as the spine of your answer — it was curated for this purpose.
2. **If no solution fits, elicit the missing constraints before recommending.** You typically need: number of concurrent users, WAN composition (wired / cellular count / satellite / Wi-Fi WAN), throughput expectations, environment (indoor / outdoor / vehicle / marine / hazardous), power (AC / DC / PoE), form factor, and budget sensitivity.
3. **Shortlist with `filter`, then verify with `show`.** Narrow to 2-3 candidates via the filter/search commands, then pull full specs for each finalist before writing the recommendation.
4. **State assumptions and caveats.** Call out any PrimeCare, Virtual WAN, or license dependency from the `note` fields. Call out "hardware revision" footnotes verbatim when they're material (throughput, RemoteSIM, etc.).

## The solutions library

`solutions/` holds curated deployment recipes as markdown files with YAML frontmatter. They exist so recurring scenarios get consistent, vetted recommendations — not fresh guesses each time.

A solution file looks like this:

```yaml
---
name: Maritime Bonded Cellular
slug: maritime-bonded-cellular
use_cases: [maritime, vessel, fishing charter, yacht, ferry]
primary_devices: ["HD2 MBX 5G", "HD4 MBX 5G"]
licenses: ["PrimeCare", "Virtual WAN (optional)"]
last_reviewed: 2026-04-17
---

Narrative goes here: the reasoning, the topology, alternate devices for smaller vessels, known gotchas, accessory list, etc.
```

When consulting solutions:

- Match on `use_cases` substrings and on device names appearing in the user's scenario.
- Quote from the narrative, but cross-check `primary_devices` against the dataset with `show` in case specs have shifted since the solution was last reviewed.
- If a solution's `last_reviewed` is older than the dataset's "last updated" date at the top of this file, mention it to the user — the recommendation is still a good starting point but specific numbers should come from the dataset.
- If the user describes a scenario that isn't covered, offer to draft a new solution file at the end — that's how the library grows.

## Grounding rules

These exist because Peplink spec sheets are dense and easy to misquote.

- **Never invent a number.** If `query.py` doesn't have it, say so. Peplink publishes performance numbers per hardware revision; making one up is actively harmful in sales or design conversations.
- **Preserve licensing language.** If the `note` mentions PrimeCare, Virtual WAN, eSIM SKU, or x.509 License Key, include it. The user cares whether a feature is standard or add-on.
- **Disambiguate product names.** BR1 Mini (HW1), BR1 Mini, and BR1 Mini 5G are three different devices. When the user is ambiguous ("BR1 Mini"), either ask or list the candidates.
- **Respect status fields.** Access points and switches carry a `Status` key in metadata (e.g., end-of-sale). Don't recommend an EOS device without flagging it.
- **Cite the datasheet, then the product page.** Every device has a `Product URL` in metadata; most (currently 84 of 103) also have a `Datasheet URL` that points at Peplink's official PDF spec sheet. When you recommend, compare, or answer a spec question about a device, prefer `Datasheet URL` for sourcing the specific numbers you cite and include `Product URL` as a secondary link for general context. If `Datasheet URL` is null for that device, fall back to `Product URL` and say "datasheet not published for this variant" so the user knows why they're not seeing the PDF.

## Data shape quick reference

- `type` is always one of `router`, `access_point`, `switch`.
- `metadata` always contains `Product URL` (if published); most devices also carry `Datasheet URL` (the PDF spec sheet), `Image URL`, and one of `Marketing Series` / `Marketing Category`. Access points and switches can also carry `Status` — respect it (EOS devices should never be recommended without a warning).
- **Routers** have nine sections: `Interfaces`, `Performance`, `Wireless details`, `Features`, `Core Functionality`, `Advanced QoS Functionality`, `VPN Functionality`, `Hardware`, `Warranty Info`.
- **Access points** and **switches** have a single flat section called `Specifications`. When comparing these to routers, expect lots of `null` cells — that's the schema, not missing data.
- Each leaf field is `{value, note?}`. The `note` is where licensing and "valid for HW2+" caveats live.

## Output shape guidance

- Use plain prose for short lookups and recommendations. A markdown table is only worth it for a true comparison (2+ devices × multiple fields).
- When the user asks for a list of candidates, keep the list tight (≤5 devices) with a one-line justification each; more is rarely helpful.
- If the user is clearly drafting a proposal or quote, offer to render the answer as a `.docx` or `.xlsx` — don't assume they want markdown.
- For "live" tracker or dashboard-style asks (e.g., "give me a page where I can keep comparing these"), suggest turning the answer into a Cowork artifact.

## Refreshing the dataset

When the user says "I have a new dataset" or similar:

1. Replace `data/peplink_all_devices.json` with the new export (same schema).
2. Re-run the datasheet enrichment so new devices get PDF links and any changed names get re-probed:

   ```bash
   python3 scripts/enrich_datasheets.py
   ```

   This probes Peplink's two known URL conventions for each device and fills in a `Datasheet URL` field on every match. Misses are expected for legacy variants and parenthetical SKUs.
3. Bump the "Dataset last updated" date at the top of this file.
4. If the JSON schema changed, read the first few lines of `data/peplink_all_devices.json`, update the "Data shape quick reference" section, and re-run the sanity queries before answering anything substantive.
