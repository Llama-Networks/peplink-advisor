---
name: # Human-readable title, e.g., "Retail Branch with Cellular Failover"
slug: # kebab-case, match the filename
use_cases:
  # Short phrases Claude should match user scenarios against.
  - # e.g., "retail store"
  - # e.g., "point of sale"
primary_devices:
  # Exact product names from the dataset. Use `query.py list` to confirm.
  - # e.g., "B One 5G"
alternate_devices:
  # Optional step-up / step-down picks.
  - # e.g., "B One"
licenses:
  # What the customer is expected to purchase alongside the hardware.
  - # e.g., "PrimeCare"
last_reviewed: # YYYY-MM-DD
---

# [Solution Name]

## The scenario

One paragraph describing the deployment shape: who the user is, what they're trying to connect, which WANs are available, and why off-the-shelf answers fall short.

## Why this pick

Two or three sentences on why the primary device is the default here. Reference specific specs (throughput, modem count, form factor) that make it the right fit.

## When to step up

When does the alternate device become the right call? (More users, heavier video, outdoor rating, etc.)

## When to step down

When is the primary pick overkill? What's the cheaper option and what does the customer give up?

## Licensing

What the customer is buying on top of the hardware, and why. Call out anything complimentary for the first year (PrimeCare) vs. permanent.

## Accessories / BOM notes

Antennas, SIMs, mounts, PoE injectors — anything the customer also needs to make this work. Keep this short; it's a prompt, not a quote.

## Known gotchas

Hardware revision differences, firmware requirements, EOS risks, anything that's bitten a previous deployment.

## Sources

- Datasheet (PDF) URL from the dataset `Datasheet URL` field (preferred)
- Product URL from the dataset `Product URL` field (fallback)
- Any internal docs or field reports you want Claude to cite
