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
  - B One 5G
alternate_devices:
  - B One
  - 5G Adapter
  - Balance 310
licenses:
  - PrimeCare
last_reviewed: 2026-05-03
---

# Retail Branch with Cellular Failover

## The scenario

A retail store, quick-serve restaurant, franchise branch, or small office with wired broadband as primary and a requirement to keep point-of-sale and payment terminals online when the wired link fails. Typical user count is 1–60 concurrent. Credit card processing is the hard constraint: even a few minutes of downtime is lost revenue.

## Why this pick

The **B One 5G** is the default for this exact shape when cellular failover is required. It has 2 Gigabit WAN ports, 4 Gigabit LAN ports, one integrated 5G modem with 2 nano-SIM slots, USB-C WAN, and 2x2 Wi-Fi 6 in a small branch form factor.

Router throughput is 1 Gbps, SpeedFusion VPN throughput is 400 Mbps unencrypted / 200 Mbps with AES, and recommended users are 1-150. That is enough headroom for POS, payment terminals, back-office traffic, light guest Wi-Fi, and a wired primary plus cellular backup design.

## When to step up

- **Balance 310** when the branch is larger, needs a stronger wired core, or expects 50-500 users. It has 2x 2.5GE WAN ports, 4x 10GE LAN ports, 4 Gbps router throughput, and 1 Gbps SpeedFusion VPN throughput with or without AES.
- Use the Balance 310 with a **5G Adapter**, external cellular router, or carrier CPE if cellular failover is still required. It is the upgrade for routing and branch-core capacity, not the integrated-cellular replacement.

## When to step down

- **B One** if the site does not need integrated cellular and has wired broadband, satellite Ethernet, a **5G Adapter**, or separate cellular CPE presented as Ethernet.
- **BR1 Pro 5G** for very small sites where cellular is the primary WAN and wired broadband is secondary or unavailable.

Do not step down below a B One for payment processing. The tiny BR1 Mini variants are excellent for kiosks and IoT but lack the SpeedFusion throughput to keep a busy POS terminal responsive during a failover event.

## Licensing

- **PrimeCare** is the right license bundle for this scenario. First year is complimentary on current hardware and it covers SpeedFusion Hot Failover (the feature that makes payment processing survive a WAN outage seamlessly rather than dropping the session), InControl 2 cloud management, and a Virtual WAN for the store's overlay network.
- Web Content Filtering is included at "Full" level on B One / B One 5G and Balance 310, useful if the customer wants to block non-business sites on guest Wi-Fi without adding a separate appliance.

## Accessories / BOM notes

- For B One 5G, plan the 5G antenna placement early. Under-counter and back-office mounts often hurt signal; use remote antennas where needed.
- Use carrier-diverse SIMs if uptime matters. Two SIMs from one carrier are not path diversity.
- Add a PoE switch if the customer also wants VoIP phones, APs, cameras, or digital signage.

## Known gotchas

- Confirm the SIM provisioning path up front. Retail chains often default to a fleet SIM provider (Inseego, Kajeet, etc.); Peplink's eSIM is great but isn't always allowed by corporate IT.
- "Hot Failover" keeps the *tunnel* alive across a WAN transition. The merchant's payment application still needs to tolerate a brief latency spike. If it doesn't, the customer is solving the wrong problem with the wrong tool.
- Balance 310 has no integrated cellular modem, no USB WAN, and no Wi-Fi AP. If cellular is required with Balance 310, use the Ethernet-based 5G Adapter, an external cellular router, or carrier CPE.

## Sources

- B One 5G datasheet: https://www.peplink.com/compare/tech-specs/b-one-5g.pdf
- B One datasheet: https://www.peplink.com/compare/tech-specs/b-one.pdf
- Balance 310 datasheet: https://www.peplink.com/compare/tech-specs/balance-310.pdf
- 5G Adapter catalog record: `data/peplink_all_devices.json` (device: "5G Adapter", SKU: "ADP-5GY-T-PRM", added 2026-05-03)
- Dataset: `data/peplink_all_devices.json` (devices: "B One 5G", "B One", "5G Adapter", "Balance 310", last updated 2026-05-03)
