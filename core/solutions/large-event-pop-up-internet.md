---
name: Large Event Pop-Up Internet
slug: large-event-pop-up-internet
use_cases:
  - event internet
  - festival
  - concert
  - pop-up internet
  - temporary event
  - vendor wifi
  - cashless payments
  - ticketing
  - event wifi
  - trade show
  - conference
  - live event
primary_devices:
  - HD4 MBX 5G
  - AP One AX
alternate_devices:
  - BR2 Pro
  - HD2 MBX 5G
  - BR1 Mini 5G
licenses:
  - CarePlan / PrimeCare (device-family dependent, for SpeedFusion and cloud management)
  - SpeedFusion Connect pooled usage or self-hosted FusionHub for bonded uplinks
  - Virtual WAN Activation License (for separate vendor, staff, production, and guest overlays)
last_reviewed: 2026-05-03
---

# Large Event Pop-Up Internet

## The scenario

A festival, conference, sporting event, or temporary venue needs internet for cashless payments, ticketing, staff communications, production users, and limited guest Wi-Fi. The WAN mix is normally cellular across multiple carriers, Starlink, and whatever fiber or fixed wireless the venue can provide. The hard problem is not raw speed; it is surviving crowd-driven cellular congestion and quickly moving capacity where it is needed.

## Why this pick

The **HD4 MBX 5G** is the default event core because it has four integrated 5G modems, eight SIM slots, 2.5 Gbps router throughput, and 600 Mbps SpeedFusion VPN throughput unencrypted / 500 Mbps encrypted. It supports 50-500 recommended users and has multiple Ethernet WANs, USB WANs, AP management, switch control, and High Availability support.

Pair it with **AP One AX** access points for the actual Wi-Fi coverage. AP One AX is Wi-Fi 6, supports 16 SSIDs, and is rated for 256 recommended concurrent users per radio. Do not rely on the MBX onboard radio for vendor areas or public coverage.

## When to step up

- Multiple **HD4 MBX 5G** units in High Availability when the event cannot tolerate a router failure or when coverage areas need separate portable kits.
- Add **SDX Pro** or FusionHub as the aggregation endpoint when production traffic, POS, and staff networks must bond back to a controlled head end.
- Use current **24 PoE 2.5G Switch Rugged** or equivalent PoE switching when APs, cameras, and payment devices are spread across the venue.

## When to step down

Use **BR2 Pro** for smaller events where two 5G modems plus Starlink are enough and the user count is under roughly 150. Use **BR1 Mini 5G** only for vehicles, ticket booths, or isolated payment points where local Wi-Fi is handled separately.

## Licensing

MBX-family deployments use CarePlan language in the dataset; BR-family deployments use PrimeCare. In either case, the design assumes active care coverage for SpeedFusion Hot Failover, Smoothing, Bandwidth Bonding, InControl, and SpeedFusion Connect usage. For larger events, quote either sufficient SpeedFusion Connect pooled usage or a self-hosted FusionHub/SDX endpoint with enough encrypted throughput.

## Accessories / BOM notes

- Carrier-diverse SIM pool; in high-density events, use multiple carriers and physically separate antennas.
- Starlink as an additional WAN, not as the only WAN.
- AP stands, outdoor APs if exposed, PoE switching, cable ramps, UPS/battery packs, and a spare router kit.
- VLANs/SSIDs for POS, ticketing, staff, production, guest, and management.

## Known gotchas

- Event failures are often RF-capacity failures, not router failures. Test local carrier performance at event load where possible and expect it to change as the crowd arrives.
- High Availability only helps if power, SIM carriers, antennas, and upstream paths are not all shared single points of failure.
- Guest Wi-Fi can consume the links that POS needs. Enforce bandwidth limits and traffic priorities before the event opens.
- If the event has streaming or timing systems, isolate them from public/vendor traffic and bond them through a known endpoint.

## Sources

- Peplink case study: https://www.peplink.com/case-studies/edc-las-vegas-festivalgoers-feast-on-peplink-and-starlink-connectivity/
- Case studies category: https://www.peplink.com/case-studies/event-internet/
- HD4 MBX 5G datasheet: https://www.peplink.com/compare/tech-specs/hd4-mbx-5g.pdf
- AP One AX datasheet: https://download.peplink.com/resources/pepwave_ap_one_ax_datasheet.pdf
- BR2 Pro datasheet: https://www.peplink.com/compare/tech-specs/br2-pro.pdf
- Dataset: `data/peplink_all_devices.json` (devices: "HD4 MBX 5G", "AP One AX", "BR2 Pro", last updated 2026-05-03)
