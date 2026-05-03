---
name: Dual 5G Quick-Service Restaurant
slug: dual-5g-quick-service-restaurant
use_cases:
  - quick service restaurant
  - qsr
  - drive through
  - drive-thru
  - restaurant
  - new store opening
  - broadband replacement
  - dual 5g
  - pos
  - point of sale
  - digital menu
primary_devices:
  - BR2 Pro
alternate_devices:
  - B One 5G
  - B One
  - Balance 310
licenses:
  - PrimeCare (SpeedFusion, InControl, InTouch, and SpeedFusion Connect usage)
  - Virtual WAN Activation License (for POS, back-office, guest, and IoT overlays)
  - AP support license AP-LC-50 if managed AP count exceeds the included limit
last_reviewed: 2026-05-03
---

# Dual 5G Quick-Service Restaurant

## The scenario

A quick-service restaurant, drive-through chain, or new retail concept needs to open before wired broadband is available, or wants to avoid expensive construction for fixed circuits. The network must keep POS, order systems, digital menus, payment terminals, cameras, VoIP, and back-office tools online. Cellular is not just failover; it may be the primary WAN.

## Why this pick

The **BR2 Pro** is the default when cellular replaces broadband because it has two integrated 5G modems, four SIM slots, 2.5G WAN/LAN flexibility, Wi-Fi 6, and 1 Gbps router throughput. SpeedFusion VPN throughput is 400 Mbps unencrypted / 200 Mbps encrypted, and recommended users are 1-150, which fits a restaurant with POS, staff, cameras, and light guest Wi-Fi.

The case-study pattern uses dual 5G, external antennas, and PoE switching to avoid months of broadband construction. This is different from a classic retail failover design: cellular is designed as production connectivity from day one.

## When to step up

- Add a PoE switch and managed APs when cameras, digital menus, kiosks, or guest Wi-Fi are part of the opening package.
- Use **HD4 MBX 5G** for a flagship or temporary high-volume site where four cellular modems are justified.
- Use a hub-and-spoke SpeedFusion design when headquarters needs secure access into every store.

## When to step down

- **B One 5G** if the site only needs one 5G modem, two wired WANs, Wi-Fi 6, and a lower-cost branch router.
- **B One** if the store has wired broadband, Starlink Ethernet, or separate cellular CPE and does not require integrated 5G.
- **Balance 310** if the site grows into a larger wired branch core. It is not the cellular-primary replacement by itself; pair it with BR2 Pro, B One 5G, or external 5G CPE if the restaurant still needs cellular WAN.

## Licensing

PrimeCare is assumed for SpeedFusion, InControl, InTouch, and the included SpeedFusion Connect usage. If POS, guest Wi-Fi, cameras, and IoT must be isolated, quote Virtual WAN licenses and VLAN work explicitly. If the chain has many stores, validate SpeedFusion peer counts and endpoint throughput before rollout.

## Accessories / BOM notes

- Two carrier-diverse 5G SIMs at minimum; four SIMs if the customer wants primary/backup carrier tiers per modem.
- External 5G antennas, especially for metal-roof restaurants or under-counter router placement.
- PoE switch for cameras, APs, kiosks, and digital signage.
- UPS for router, switch, POS network gear, and carrier CPE.

## Known gotchas

- "Unlimited" cellular plans often have deprioritization, hotspot, or router-use restrictions. Validate the plan type before using 5G as primary WAN.
- Restaurant cameras and guest Wi-Fi can overwhelm cellular. Apply traffic shaping and isolate business-critical POS/order systems.
- Put antennas where signal is clean, not where cabling is easiest.
- If broadband arrives later, decide whether cellular remains active-active, hot failover, or a metered tertiary path.

## Sources

- Peplink case study: https://www.peplink.com/case-studies/peplink-connectivity-rapidly-deployed-for-quick-service-restaurant-salad-and-go/
- Case studies category: https://www.peplink.com/case-studies/latest
- BR2 Pro datasheet: https://www.peplink.com/compare/tech-specs/br2-pro.pdf
- B One 5G datasheet: https://www.peplink.com/compare/tech-specs/b-one-5g.pdf
- B One datasheet: https://www.peplink.com/compare/tech-specs/b-one.pdf
- Balance 310 datasheet: https://www.peplink.com/compare/tech-specs/balance-310.pdf
- Dataset: `data/peplink_all_devices.json` (devices: "BR2 Pro", "B One 5G", "B One", "Balance 310", last updated 2026-05-03)
