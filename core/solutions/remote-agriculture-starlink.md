---
name: Remote Agriculture with Starlink and 5G
slug: remote-agriculture-starlink
use_cases:
  - farming
  - agriculture
  - greenhouse
  - arctic agriculture
  - remote agriculture
  - farm internet
  - ranch
  - environmental sensors
  - off-grid
  - solar powered
  - starlink farm
primary_devices:
  - BR2 Pro
alternate_devices:
  - Dome Pro Duo
  - B One 5G
  - BR1 Pro 5G
licenses:
  - PrimeCare (SpeedFusion, InControl, InTouch, and SpeedFusion Connect usage)
  - Virtual WAN Activation License (for sensors, cameras, operations, and guest overlays)
  - SpeedFusion Connect usage or self-hosted FusionHub for bonded satellite/cellular
last_reviewed: 2026-05-03
---

# Remote Agriculture with Starlink and 5G

## The scenario

A farm, greenhouse, ranch, research site, or off-grid agriculture project needs reliable internet for environmental sensors, cameras, automation systems, staff devices, remote monitoring, and collaboration. The site may depend on Starlink, cellular, solar or wind power, and rugged enclosures because there is no local broadband.

## Why this pick

The **BR2 Pro** is the default because it gives dual 5G modems, four SIM slots, Wi-Fi 6, USB WAN for another uplink, GPS, and 1 Gbps router throughput in a compact mobile router. SpeedFusion VPN throughput is 400 Mbps unencrypted / 200 Mbps encrypted, and recommended users are 1-150. It can bond or fail over between Starlink and cellular while remaining manageable through InControl.

## When to step up

- **Dome Pro Duo** when the cellular radios need to live outdoors on a pole or container roof. It is IP67, has two 5G modems, four SIM slots, PoE input, and GPS.
- Add **AP One AX** or outdoor APs when workers need Wi-Fi across buildings or greenhouses.
- Use **SDX** or **BR2 Pro plus external switching** when the site grows into multiple buildings, cameras, and automation controllers.

## When to step down

Use **B One 5G** for a smaller fixed farm office with one 5G modem, Wi-Fi 6, two wired WANs, and lower cost. Use **BR1 Pro 5G** for a mobile farm vehicle, field trailer, or single-greenhouse deployment that only needs one cellular modem plus Starlink.

## Licensing

PrimeCare is assumed for SpeedFusion features, InControl, and SpeedFusion Connect usage. If sensors, cameras, staff devices, and public/guest Wi-Fi share the same WANs, use VLANs and Virtual WANs to keep automation and monitoring separate from user traffic.

## Accessories / BOM notes

- Starlink with clear sky view and weatherproof cabling.
- Solar/wind/battery system sized for Starlink, Peplink router, APs, cameras, and enclosure climate control.
- External cellular antenna or Dome Pro Duo for weak-signal rural sites.
- Environmental enclosure, grounding, surge protection, and remote power cycling.

## Known gotchas

- Power is the design constraint in off-grid agriculture. The router is only a small part of total load.
- Greenhouses and metal containers can block RF. Put the cellular antenna or Dome outside.
- Sensor traffic is low bandwidth but high value; protect it from worker/guest Wi-Fi and camera uploads.
- If the site is in an extreme climate, verify operating-temperature ranges for every component, not just the router.

## Sources

- Peplink case study: https://www.peplink.com/case-studies/reliable-year-round-sustainable-arctic-agriculture-powered-by-peplink-and-starlink/
- Case studies category: https://www.peplink.com/case-studies/starlink/
- BR2 Pro datasheet: https://www.peplink.com/compare/tech-specs/br2-pro.pdf
- Dome Pro Duo datasheet: https://www.peplink.com/compare/tech-specs/dome-pro-duo.pdf
- B One 5G datasheet: https://www.peplink.com/compare/tech-specs/b-one-5g.pdf
- Dataset: `data/peplink_all_devices.json` (devices: "BR2 Pro", "Dome Pro Duo", "B One 5G", "BR1 Pro 5G", last updated 2026-05-03)
