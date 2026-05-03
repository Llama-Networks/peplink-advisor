---
name: Public Transport Passenger Wi-Fi
slug: public-transport-passenger-wifi
use_cases:
  - public transport
  - bus wifi
  - train wifi
  - passenger wifi
  - transit wifi
  - coach bus
  - school bus
  - fleet wifi
  - vehicle wifi
  - onboard wifi
primary_devices:
  - BR1 Pro 5G
alternate_devices:
  - Transit Duo Pro
  - BR2 Pro
  - HD4 MBX 5G
licenses:
  - PrimeCare (SpeedFusion, InControl, InTouch, and SpeedFusion Connect usage)
  - FusionHub license or hosted SpeedFusion endpoint for fleet bonding
  - Virtual WAN Activation License (if CCTV, ticketing, guest Wi-Fi, and telemetry need separate overlays)
last_reviewed: 2026-05-03
---

# Public Transport Passenger Wi-Fi

## The scenario

A bus, coach, rail, or school transport fleet needs passenger Wi-Fi plus operational connectivity for ticketing, telemetry, CCTV, driver systems, and remote management. Routes cross rural or urban coverage gaps, and the operator wants fewer one-off subscriptions by consolidating onboard services behind one managed router.

## Why this pick

The **BR1 Pro 5G** is the default for a single vehicle because it combines one 5G modem, two SIM slots, Wi-Fi 6, GPS, ignition sensing, and DC input in a compact mobile router. It supports 1-150 recommended users with 1 Gbps router throughput and 400 Mbps SpeedFusion VPN throughput unencrypted / 200 Mbps encrypted. It is enough for a bus with Starlink or another secondary WAN, especially when SpeedFusion tunnels back to FusionHub.

## When to step up

- **Transit Duo Pro** when two cellular modems are required in a transport-focused form factor and Starlink is not always present.
- **BR2 Pro** when two 5G modems, four SIM slots, serial, USB WAN, and local AP/switch control are needed.
- **HD4 MBX 5G** for trains, command vehicles, or high-capacity coaches where four 5G modems and 50-500 recommended users are justified.

## When to step down

Use **BR1 Mini 5G** only for low-user-count service vehicles or isolated devices. For passenger Wi-Fi, the lack of integrated Wi-Fi AP and GPS makes it a poor default unless another AP and tracking system are already installed.

## Licensing

PrimeCare is assumed. It covers SpeedFusion Hot Failover, Smoothing, Bandwidth Bonding, InControl, InTouch, and SpeedFusion Connect usage on the BR/Transit class devices. Use a self-hosted FusionHub when the fleet needs a stable fixed endpoint, private addressing, or more predictable backhaul than a shared hosted service.

## Accessories / BOM notes

- Roof-mounted mobility antenna sized for 5G and Wi-Fi/GPS needs.
- Starlink Mini or other LEO terminal when routes have long cellular gaps.
- DC wiring to vehicle power, ignition sensing, and proper fuse protection.
- Captive portal and bandwidth limits for passenger SSID.
- VLANs for passenger Wi-Fi, ticketing, telemetry, CCTV, and management.

## Known gotchas

- Vehicle body materials can hurt RF badly. Roof antennas are not optional for reliable fleet Wi-Fi.
- Starlink on vehicles may have service-plan and mounting constraints; verify before quoting it as a standard WAN.
- Passenger Wi-Fi needs policy. Without per-user shaping, entertainment traffic can starve ticketing and telemetry.
- If route visibility matters, choose a device with GPS. BR1 Mini 5G does not provide GPS; BR1 Pro 5G does.

## Sources

- Peplink case study: https://www.peplink.com/case-studies/peplink-and-starlink-drive-the-future-of-public-transport-connectivity/
- Case studies category: https://www.peplink.com/case-studies/car-internet/
- BR1 Pro 5G datasheet: https://www.peplink.com/compare/tech-specs/br1-pro-5g.pdf
- BR2 Pro datasheet: https://www.peplink.com/compare/tech-specs/br2-pro.pdf
- Dataset: `data/peplink_all_devices.json` (devices: "BR1 Pro 5G", "Transit Duo Pro", "BR2 Pro", "HD4 MBX 5G", last updated 2026-05-03)
