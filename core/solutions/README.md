# Solutions Library

Curated deployment recipes. Each file captures a recurring scenario (maritime, retail, first responder, etc.) and pins the devices, licenses, topology, and gotchas so the skill gives consistent answers instead of rolling the dice every time.

## Current solutions

- `broadcast-ob-vehicle-bonded-5g.md` - bonded 5G for outside-broadcast vehicles, live production, and DSNG alternatives.
- `dual-5g-quick-service-restaurant.md` - cellular-primary restaurant and drive-through openings where broadband is delayed or too expensive.
- `large-event-pop-up-internet.md` - temporary event, festival, vendor, ticketing, and guest Wi-Fi designs using cellular, Starlink, fiber, and APs.
- `maritime-bonded-cellular.md` - coastal vessel and passenger connectivity using multi-carrier bonded cellular.
- `public-safety-field-kit.md` - portable Starlink-plus-5G kit for incident command and emergency response.
- `public-transport-passenger-wifi.md` - bus, coach, train, school-bus, and fleet Wi-Fi with operational traffic segregation.
- `remote-agriculture-starlink.md` - off-grid farm, greenhouse, ranch, and research-site connectivity with Starlink and 5G.
- `remote-industrial-scada-monitoring.md` - distributed utility, pump-station, pipeline, and industrial telemetry networks.
- `remote-mining-construction-hub.md` - movable mining, construction, and remote machinery hubs with Starlink, outdoor 5G, switching, and Wi-Fi.
- `retail-5g-primary-dual-cellular.md` - retail 5G-primary designs using B One 5G, single-radio SIM failover, 5G Dongle over USB-C, or 5G Adapter over Ethernet.
- `retail-branch-cellular-failover.md` - small branch and retail POS continuity with wired primary and cellular failover.
- `starlink-remote-site-failover.md` - Starlink-primary remote sites with cellular failover and InControl management.
- `telemedicine-rural-clinic.md` - remote clinic, telemedicine, and healthcare outreach connectivity.

The 2026-05-03 expansion was grounded in Peplink's case-study categories: Starlink, event internet, ship internet, streaming internet, smart construction, school internet, public safety, car/transport internet, hospital/telemedicine, branch/retail, WAN failover, logistics, warehouse, farming, and related product/model filters.

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
