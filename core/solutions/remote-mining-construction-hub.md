---
name: Remote Mining and Construction Connectivity Hub
slug: remote-mining-construction-hub
use_cases:
  - mining
  - remote mining
  - construction site
  - smart construction
  - remote camp
  - tactical hub
  - job site internet
  - construction trailer
  - site office
  - remote machinery
  - autonomous machinery
primary_devices:
  - SDX
  - Dome Pro Duo
  - AP One AX
  - 24 PoE 2.5G Switch Rugged
alternate_devices:
  - BR2 Pro
  - SDX Pro
  - HD4 MBX 5G
licenses:
  - CarePlan on SDX / SDX Pro for SpeedFusion and cloud management
  - PrimeCare on BR2 Pro or Dome Pro Duo nodes
  - SpeedFusion Connect usage or self-hosted FusionHub / SDX endpoint
  - Virtual WAN Activation License (for worker Wi-Fi, OT, camera, and admin overlays)
last_reviewed: 2026-05-03
---

# Remote Mining and Construction Connectivity Hub

## The scenario

A mine, remote construction site, industrial trailer, or autonomous-machinery project needs a movable network hub. The WAN mix may include multiple Starlink kits, outdoor 5G domes, fiber between trailers, and local Wi-Fi. Users include workers, operations, remote monitoring, cameras, machine-control teams, and corporate systems. The site is harsh, bandwidth-heavy, and expensive to service.

## Why this pick

The **SDX** is the default core for a larger movable hub because it can aggregate many WANs, supports 12 Gbps router throughput, 1 Gbps SpeedFusion VPN throughput unencrypted / 600 Mbps encrypted, and supports 500-2000 recommended users. It can manage APs/switches and use FlexModule Plus options for cellular expansion where needed.

Use **Dome Pro Duo** for outdoor 5G capture at the edge of the hub. It has two integrated 5G modems, four SIM slots, IP67 outdoor metal enclosure, PoE input, 1 Gbps router throughput, and 400 Mbps SpeedFusion VPN throughput unencrypted / 200 Mbps encrypted. Pair **AP One AX** for local Wi-Fi 6 and **24 PoE 2.5G Switch Rugged** for PoE distribution and fiber handoff in harsh environments.

## When to step up

- **SDX Pro** when the hub needs more expansion slots, dual hot-swap power supplies, 24 Gbps router throughput, 800 SpeedFusion VPN peers, or edge compute storage.
- **HD4 MBX 5G** when the core must be vehicle-mounted, DC powered, cellular-heavy, and able to provide integrated PoE to local devices.
- Multiple Dome Pro Duo units when the site needs physical antenna separation or carrier diversity in more than one direction.

## When to step down

Use **BR2 Pro** for a small site trailer or remote machinery command post. It gives two 5G modems, four SIM slots, serial RS-232, Wi-Fi 6, 1 Gbps router throughput, and 1-150 recommended users without the rack core and switch stack.

## Licensing

The hub assumes active care coverage across routers. SDX uses CarePlan language in the dataset; Dome Pro Duo and BR2 Pro use PrimeCare. Quote SpeedFusion Connect usage or a self-hosted FusionHub/SDX endpoint based on the number of WANs and expected bonded traffic. Add Virtual WAN licenses when OT, admin, guest, camera, and contractor networks need separate overlays.

## Accessories / BOM notes

- Starlink Flat High Performance or equivalent LEO terminals where cellular is not enough.
- SIM Injector for outdoor domes when the SIM pool must live in the trailer rather than on the mast.
- Rugged PoE switching, SFP/SFP+ optics, fiber between trailers, UPS/generator integration, and environmental controls.
- Outdoor-rated mounts, mast hardware, grounding, and lightning protection.

## Known gotchas

- SDX and SDX Pro are indoor rack devices with 32-104 F / 0-40 C operating ranges. Put them in a conditioned trailer or enclosure.
- Dome Pro Duo PoE output requires the right PoE input budget. Confirm the powering design before promising it will also power downstream devices.
- Multiple Starlinks are only useful when they have clean sky view and independent power/cabling.
- Remote machinery control needs latency and jitter validation, not just throughput. Use SpeedFusion policy and QoS around the control and video paths.

## Sources

- Peplink case study: https://www.peplink.com/case-studies/bridging-the-divide-reliable-connectivity-for-remote-mining-operations-with-peplink/
- Peplink case study: https://www.peplink.com/case-studies/network-innovations-transforms-remote-machinery-control-with-peplink/
- Case studies category: https://www.peplink.com/case-studies/smart-construction/
- SDX datasheet: https://www.peplink.com/compare/tech-specs/sdx.pdf
- Dome Pro Duo datasheet: https://www.peplink.com/compare/tech-specs/dome-pro-duo.pdf
- 24 PoE 2.5G Switch Rugged product page: https://www.peplink.com/products/wifi-poe/switch-series/
- Dataset: `data/peplink_all_devices.json` (devices: "SDX", "Dome Pro Duo", "AP One AX", "24 PoE 2.5G Switch Rugged", "BR2 Pro", last updated 2026-05-03)
