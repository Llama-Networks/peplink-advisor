---
name: Retail Branch with Cellular Failover
slug: retail-branch-cellular-failover
use_cases:
  - retail
  - retail store
  - point of sale
  - pos
  - branch office
  - small branch
  - franchise
  - cellular failover
  - 4g backup
  - 5g backup
primary_devices:
  - Balance 20X
alternate_devices:
  - B One
  - B One Plus
  - Balance 30 PRO
licenses:
  - PrimeCare
last_reviewed: 2026-04-17
---

# Retail Branch with Cellular Failover

## The scenario

A retail store, quick-serve restaurant, franchise branch, or small office with wired broadband as primary and a requirement to keep point-of-sale and payment terminals online when the wired link fails. Typical user count is 1–60 concurrent. Credit card processing is the hard constraint: even a few minutes of downtime is lost revenue.

## Why this pick

The **Balance 20X** is the long-standing default for this exact shape. It has one Gigabit WAN, four Gigabit LAN ports, and an integrated cellular modem, and — crucially — a **FlexModule Mini** expansion slot that lets the customer pick their cellular category (CAT-4 up to CAT-20 or 5G) without changing the chassis. That means you can ship a CAT-4 today and upgrade to 5G later without a forklift.

Router throughput is 900 Mbps, SpeedFusion VPN throughput is 100 Mbps unencrypted / 60 Mbps with AES — plenty for a retail branch where the cellular failover is the limiting factor, not the router. Recommended users 1–60. Two SIM slots standard, up to four with the FlexModule.

## When to step up

- **B One Plus** if the customer needs 2 WAN ports (e.g., fiber + cable as dual-wired) alongside cellular backup. The B One Plus has 2 GE WAN / 4 GE LAN with an integrated modem and still fits a small branch form factor.
- **Balance 30 PRO** if the customer wants 3 WAN paths (dual wired + cellular) and is willing to skip the module flexibility of the 20X for the simpler hard-spec. Best when cellular backup is a "nice to have" rather than the main event.

## When to step down

- **B One** if the customer doesn't need the FlexModule and CAT-4 is forever-sufficient. Lower cost, same general feature set.
- **BR1 Pro** series for very small sites (1–5 users) where cellular is the primary and wired is the secondary — flips the topology.

Do not step down below a B One for payment processing. The tiny BR1 Mini variants are excellent for kiosks and IoT but lack the SpeedFusion throughput to keep a busy POS terminal responsive during a failover event.

## Licensing

- **PrimeCare** is the right license bundle for this scenario. First year is complimentary on current hardware and it covers SpeedFusion Hot Failover (the feature that makes payment processing survive a WAN outage seamlessly rather than dropping the session), InControl 2 cloud management, and a Virtual WAN for the store's overlay network.
- Web Content Filtering is included at "Full" level on Balance 20X — useful if the customer wants to block non-business sites on guest Wi-Fi without adding a separate appliance.

## Accessories / BOM notes

- **FlexModule Mini** sized to the carrier: CAT-12 or CAT-18 is usually the sweet spot today. 5G is worth it only if the site actually has 5G coverage — verify via the carrier's coverage map, not the brochure.
- One or two cellular antennas depending on where the unit will be mounted. Under-counter enclosures hurt signal; plan for a remote antenna.
- A PoE switch if the customer also wants VoIP phones or APs — the 20X itself doesn't provide PoE.

## Known gotchas

- Confirm the SIM provisioning path up front. Retail chains often default to a fleet SIM provider (Inseego, Kajeet, etc.); Peplink's eSIM is great but isn't always allowed by corporate IT.
- "Hot Failover" keeps the *tunnel* alive across a WAN transition. The merchant's payment application still needs to tolerate a brief latency spike. If it doesn't, the customer is solving the wrong problem with the wrong tool.
- Balance 20X is mature hardware. It's not EOS at time of last review, but confirm against Peplink's current price list before a large rollout.

## Sources

- Datasheet (PDF): https://www.peplink.com/compare/tech-specs/balance-20x.pdf
- Product page: https://peplink.com/products/balance-20x/
- Dataset: `data/peplink_all_devices.json` (device: "Balance 20X", last updated 2026-04-17)
