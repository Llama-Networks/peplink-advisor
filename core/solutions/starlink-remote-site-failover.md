---
name: Starlink Remote Site with Cellular Failover
slug: starlink-remote-site-failover
use_cases:
  - starlink
  - remote site
  - remote office
  - remote cabin
  - remote pipeline
  - pipeline
  - oil and gas
  - backup to starlink
  - cellular backup
  - satellite failover
  - unmanned site
primary_devices:
  - BR1 Mini 5G
alternate_devices:
  - B One 5G
  - BR1 Pro 5G
  - BR2 Pro
licenses:
  - PrimeCare (required for Ethernet WAN, SpeedFusion Hot Failover, Smoothing, and Bandwidth Bonding on BR1 Mini 5G)
  - Feature Pack License MAX-BR1-MINI-LC-FP (perpetual alternative for BR1 Mini feature enablement)
  - Virtual WAN Activation License (if additional virtual WAN endpoints are needed beyond the complimentary allocation)
last_reviewed: 2026-05-03
---

# Starlink Remote Site with Cellular Failover

## The scenario

A remote site has Starlink as the primary WAN, but the operator needs a cellular safety net for telemetry, cameras, IoT sensors, VoIP, or basic staff access when the satellite link drops. Typical examples are pipeline sites, water or utility assets, seasonal cabins, temporary field offices, and off-grid equipment shelters. Wired broadband is unavailable or not worth building, and truck rolls are expensive.

## Why this pick

The **BR1 Mini 5G** is the default for a single unattended site because it is compact, low power, and rugged enough for enclosures. It gives one 5G modem with two SIM slots, 300 Mbps router throughput, and 80 Mbps SpeedFusion VPN throughput unencrypted / 60 Mbps with 256-bit AES. Recommended users are 1-60, which is enough for telemetry, remote access, and a few cameras.

This is a control-plane and resilience design, not a "make Starlink faster" design. Starlink remains the high-capacity path; the Peplink box keeps management and essential traffic alive over 5G and gives InControl visibility when the site is hard to reach.

## When to step up

- **B One 5G** when the site is a small staffed office or trailer and needs integrated Wi-Fi 6, two wired WAN ports, or AP/switch control. It supports 1 Gbps router throughput and 400 Mbps SpeedFusion VPN throughput unencrypted / 200 Mbps encrypted.
- **BR1 Pro 5G** when GPS tracking, Wi-Fi 6, higher transmit power, or stronger mobile-router features matter.
- **BR2 Pro** when the site needs two active 5G modems, four SIM slots, serial RS-232, or a larger local LAN. This is the better default when cellular is expected to carry real traffic, not just failover.

## When to step down

Use non-5G **BR1 Mini** only for low-bandwidth LTE telemetry where 5G coverage is not present and the customer is optimizing fleet cost. Do not use a Mini as the whole guest Wi-Fi experience: BR1 Mini 5G has no Wi-Fi AP radio, no GPS, and no AP/switch controller.

## Licensing

PrimeCare is not optional in this pattern unless the customer intentionally buys the perpetual feature pack instead. For BR1 Mini 5G, Ethernet WAN, Wi-Fi WAN, Hot Failover, and Smoothing are enabled by PrimeCare, complimentary for the first year, or by the BR1 Mini feature pack. PrimeCare also includes 500 GB/year of SpeedFusion Connect usage on BR1 Mini 5G.

If the site needs multiple overlays, plan for Virtual WAN Activation Licenses. If the hub is self-hosted, size FusionHub or the head-end router for the encrypted throughput of all remote sites combined.

## Accessories / BOM notes

- Starlink Ethernet adapter or a Starlink model with Ethernet handoff.
- Outdoor enclosure, DIN mounting as needed, surge protection, and managed power reboot for Starlink.
- External 5G/LTE antennas if the router is inside a metal cabinet.
- Dual-carrier SIMs. A second SIM from the same carrier is not real diversity.

## Known gotchas

- BR1 Mini 5G can do the job, but the PrimeCare/feature-pack dependency is the gotcha. Confirm the license path before quoting a Starlink failover design.
- Starlink and cellular often fail for different reasons. That is useful, but the cellular path still needs real signal testing at the enclosure location.
- For camera-heavy sites, fail over only the critical VLAN or camera event stream. Letting all video move to cellular can burn data quickly.
- Solar or battery sizing must include Starlink, the Peplink device, heaters/fans, and any cameras or radios. The router alone is not the power budget.

## Sources

- Peplink case study: https://www.peplink.com/case-studies/hyperlink-boosts-scada-performance-with-peplink-in-remote-pipeline-operations/
- Case studies category: https://www.peplink.com/case-studies/starlink/
- BR1 Mini 5G datasheet: https://www.peplink.com/compare/tech-specs/br1-mini-5g.pdf
- B One 5G datasheet: https://www.peplink.com/compare/tech-specs/b-one-5g.pdf
- BR2 Pro datasheet: https://www.peplink.com/compare/tech-specs/br2-pro.pdf
- Dataset: `data/peplink_all_devices.json` (devices: "BR1 Mini 5G", "B One 5G", "BR1 Pro 5G", "BR2 Pro", last updated 2026-05-03)
