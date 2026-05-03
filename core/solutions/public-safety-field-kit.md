---
name: Public Safety Rapid Field Kit
slug: public-safety-field-kit
use_cases:
  - public safety
  - emergency response
  - first responder
  - incident command
  - fire department
  - police
  - rescue
  - command post
  - disaster response
  - field kit
  - portable starlink
primary_devices:
  - BR1 Mini 5G
alternate_devices:
  - BR1 Pro 5G
  - BR2 Pro
  - HD4 MBX 5G
licenses:
  - PrimeCare (or BR1 Mini feature pack for perpetual failover features)
  - SpeedFusion Connect usage or public-safety-owned FusionHub endpoint
  - Virtual WAN Activation License (if separate public-safety overlays are required)
last_reviewed: 2026-05-03
---

# Public Safety Rapid Field Kit

## The scenario

A fire, EMS, police, emergency management, or search-and-rescue team needs a carryable network kit for incident command. The kit may include Starlink Mini, 5G/LTE, battery power, and a small enclosure so responders can bring up VoIP, mapping, dispatch tools, live video, forms, and Wi-Fi in areas where local infrastructure is damaged or absent.

## Why this pick

The **BR1 Mini 5G** is the default for a lightweight Starlink-plus-5G kit because it is small, low power, and rated from -40 to 149 F / -40 to 65 C. It supports 1-60 recommended users and can use SpeedFusion Hot Failover to move between Starlink and cellular paths. Router throughput is 300 Mbps, with 80 Mbps SpeedFusion VPN throughput unencrypted / 60 Mbps encrypted.

This is a rapid deployment design: keep the kit simple, known-good, preconfigured in InControl, and ready for battery operation. The case-study pattern is a tripod or portable enclosure where Starlink provides primary bandwidth and Peplink provides cellular failover and centralized control.

## When to step up

- **BR1 Pro 5G** if the team needs GPS fleet tracking, integrated Wi-Fi 6, higher SpeedFusion throughput, or a stronger all-in-one mobile router.
- **BR2 Pro** if the kit needs two active 5G modems, four SIM slots, serial RS-232, USB WAN, and AP/switch control.
- **HD4 MBX 5G** for a larger command trailer or EOC vehicle with multiple carriers, PoE devices, and 50-500 users.

## When to step down

Do not step down below BR1 Mini 5G for a Starlink-first public-safety kit unless the need is fixed LTE telemetry. The non-5G Mini can work for low-bandwidth devices, but responder workflows increasingly include video, maps, and cloud apps. For a one-person vehicle with only MDT/AVL needs, BR1 Pro 5G is often a better fit than Mini because of GPS and onboard Wi-Fi.

## Licensing

BR1 Mini 5G requires PrimeCare or the feature pack to enable Ethernet WAN, Hot Failover, Smoothing, and Bandwidth Bonding. PrimeCare also provides the SpeedFusion Connect allowance. Agencies that do not want cloud-hosted VPN should use their own FusionHub or head-end router and explicitly validate CJIS/security requirements.

## Accessories / BOM notes

- Starlink Mini or other LEO terminal with Ethernet handoff.
- Battery sized for the whole kit, not just the router.
- Weather-resistant enclosure, tripod or mast, cable strain relief, and spare power cables.
- Agency-owned SIMs across at least two carriers where possible.
- External AP if responders need usable Wi-Fi beyond the immediate case.

## Known gotchas

- BR1 Mini 5G does not include GPS or Wi-Fi AP. If those are expected, choose BR1 Pro 5G or add external devices.
- Public-safety kits need operational procedures: who turns it on, how SSIDs are named, who monitors data use, and how it is recovered after the incident.
- Battery runtime claims must be tested with Starlink, the Peplink router, enclosure fans/heaters, and APs running together.
- Keep a cached config export and spare SIMs. Incident response is the wrong time to discover the account or SIM was suspended.

## Sources

- Peplink case study: https://www.peplink.com/case-studies/seamless-field-connectivity-for-semrecc-peplink-and-starlink-integration-in-emergency-operations/
- Case studies category: https://www.peplink.com/case-studies/public-safety-network/
- BR1 Mini 5G datasheet: https://www.peplink.com/compare/tech-specs/br1-mini-5g.pdf
- BR1 Pro 5G datasheet: https://www.peplink.com/compare/tech-specs/br1-pro-5g.pdf
- BR2 Pro datasheet: https://www.peplink.com/compare/tech-specs/br2-pro.pdf
- Dataset: `data/peplink_all_devices.json` (devices: "BR1 Mini 5G", "BR1 Pro 5G", "BR2 Pro", last updated 2026-05-03)
