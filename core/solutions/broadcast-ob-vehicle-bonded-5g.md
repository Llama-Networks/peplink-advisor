---
name: Broadcast OB Vehicle Bonded 5G
slug: broadcast-ob-vehicle-bonded-5g
use_cases:
  - broadcast
  - live stream
  - live streaming
  - outside broadcast
  - ob vehicle
  - news truck
  - remote production
  - dsng alternative
  - sports broadcast
  - field production
primary_devices:
  - HD4 MBX 5G
alternate_devices:
  - HD2 MBX 5G
  - BR2 Pro
  - SDX Pro
licenses:
  - CarePlan (for MBX SpeedFusion features and cloud management)
  - SpeedFusion license expansion if the OB fleet exceeds default peer limits
  - FusionHub or SDX Pro head-end licensing / care for master-control aggregation
last_reviewed: 2026-05-03
---

# Broadcast OB Vehicle Bonded 5G

## The scenario

A broadcaster, production company, or live-streaming team needs resilient uplink from outside-broadcast vehicles, temporary production locations, or mobile studios. Satellite may still exist for special cases, but the goal is to reduce reliance on expensive DSNG uplinks by bonding 5G/LTE carriers and backhauling securely to master control.

## Why this pick

The **HD4 MBX 5G** is the default OB-vehicle router because it gives four concurrent 5G modems, eight SIM slots, GPS, DC input, terminal-block power, ignition sensing, and 8x 802.3at PoE+ output when properly powered. Router throughput is 2.5 Gbps and SpeedFusion VPN throughput is 600 Mbps unencrypted / 500 Mbps encrypted, leaving headroom for bonded contribution feeds.

The design usually pairs vehicle MBX units with a central **SDX Pro** or FusionHub endpoint. The field router needs cellular diversity; the head end needs stable bandwidth, SpeedFusion capacity, and clean handoff into the production network.

## When to step up

- Add **SDX Pro** in High Availability at master control for larger fleets, central policy, and many SpeedFusion peers.
- Use multiple HD4 kits per site when production, engineering, and general internet need physically separate failure domains.
- Add Starlink or fixed venue Ethernet as extra WAN paths, especially outside dense urban carrier coverage.

## When to step down

Use **HD2 MBX 5G** when two cellular modems are enough and the vehicle count is small. Use **BR2 Pro** for a compact live-streaming kit with two 5G modems, four SIM slots, Wi-Fi 6, and 1-150 recommended users. Do not step down to a single-modem unit for paid live production unless another independent WAN is always present.

## Licensing

Keep CarePlan active on MBX devices for SpeedFusion features and cloud management. The HD4 MBX 5G default peer count is 3, with optional SpeedFusion licenses to reach 20 or 50 peers. Size the head end for aggregate encrypted throughput, not per-vehicle peak marketing throughput.

## Accessories / BOM notes

- Vehicle roof antennas sized for the number of modem chains and local mounting constraints.
- SDX Pro, FusionHub, or another controlled endpoint at master control.
- DC power harnesses, ignition-sensing wiring, and UPS/power conditioning in the truck.
- Separate VLANs for contribution feeds, intercom/VoIP, engineering, and general internet.

## Known gotchas

- The HD4 MBX 5G onboard Wi-Fi is 2x2 Wi-Fi 5. Use dedicated access points for crew Wi-Fi.
- Carrier bonding is only as good as the carriers available at the shoot. Scout locations and have SIMs from more than two providers when production value justifies it.
- WAN Smoothing can protect jitter-sensitive video, but it consumes duplicate bandwidth. Use it intentionally for the feed, not for every user VLAN.
- Confirm eSIM support against hardware revision and firmware before promising remote SIM changes.

## Sources

- Peplink case study: https://www.peplink.com/case-studies/smart-informatics-equips-czech-tv-to-broadcast-beyond-boundaries-with-peplink/
- Case studies category: https://www.peplink.com/case-studies/streaming-internet/
- HD4 MBX 5G datasheet: https://www.peplink.com/compare/tech-specs/hd4-mbx-5g.pdf
- SDX Pro datasheet: https://www.peplink.com/compare/tech-specs/sdx-pro.pdf
- BR2 Pro datasheet: https://www.peplink.com/compare/tech-specs/br2-pro.pdf
- Dataset: `data/peplink_all_devices.json` (devices: "HD4 MBX 5G", "SDX Pro", "BR2 Pro", last updated 2026-05-03)
