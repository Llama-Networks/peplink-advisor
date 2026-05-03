---
name: Retail 5G Primary with SIM Failover
slug: retail-5g-primary-dual-cellular
use_cases:
  - retail 5g
  - 5g primary retail
  - cellular primary retail
  - wireless primary retail
  - fixed wireless retail
  - sim failover
  - dual sim failover
  - b one 5g
  - 5g dongle
  - peplink 5g dongle
  - 5g adapter
  - dual cellular retail
  - point of sale
  - pos
  - payment terminals
  - pop-up retail
primary_devices:
  - B One 5G
  - 5G Dongle
alternate_devices:
  - 5G Adapter
  - B One
  - BR2 Pro
  - Balance 310
licenses:
  - PrimeCare
last_reviewed: 2026-05-03
---

# Retail 5G Primary with SIM Failover

## The scenario

A retail store, seasonal shop, mall kiosk, pop-up site, or small branch needs 5G as the primary WAN because wired broadband is delayed, expensive, unreliable, or not available. The site still needs payment terminals, POS, back-office devices, inventory systems, staff Wi-Fi, and sometimes a small guest Wi-Fi network. The design goal is not maximum speed; it is keeping business-critical traffic online when the primary carrier, SIM account, or wired handoff has a problem.

## Why this pick

The **B One 5G** is the default retail edge for this shape. It has 2 Gigabit WAN ports, 4 Gigabit LAN ports, one integrated 5G modem with 2 nano-SIM slots, USB-C WAN, 2x2 Wi-Fi 6, 1 Gbps router throughput, and 400 Mbps SpeedFusion VPN throughput unencrypted / 200 Mbps encrypted. Recommended users are 1-150, which fits most stores with POS, payment, staff devices, and light guest Wi-Fi.

Use the integrated 5G modem's two SIM slots when the customer needs **SIM failover in a single-radio design**. That is a good fit when the store wants a primary carrier plus a standby carrier or eSIM, but does not need two cellular links active at the same time.

Add a **5G Dongle** when the B One 5G needs a second cellular WAN over USB-C. The 5G Dongle is a newer Peplink product, not a generic accessory; in this topology it acts as the second cellular WAN for the B One 5G. This gives the site one embedded 5G modem plus one USB-C 5G product, so WAN policies can fail over or balance across two cellular radios instead of only switching SIMs inside one radio.

Use the **5G Adapter** when Ethernet is the better handoff. It is the larger product with an Ethernet port, which makes it a cleaner fit for routers or branch cores that should receive cellular as Ethernet WAN rather than USB-C.

## When to step up

- **BR2 Pro** when cellular is the production WAN from day one and the customer wants the cleanest dual-cellular hardware design. It has two integrated 5G modems, four SIM slots, Wi-Fi 6, 2.5G WAN/LAN flexibility, GPS, USB WAN, and serial. Use this instead of a B One 5G plus adapter when the deployment is not cost-sensitive and dual cellular is a requirement, not an add-on.
- **Balance 310** when the store grows into a larger branch core with 50-500 users, stronger wired routing, 10GE LAN, or more headroom for APs, switches, cameras, and segmentation. Balance 310 has no integrated cellular and no USB WAN, so pair it with a 5G Adapter, external 5G router, carrier CPE, or other Ethernet cellular handoff if cellular remains part of the WAN design.

## When to step down

Use **B One** if the customer does not need integrated 5G and already has wired broadband, Starlink Ethernet, or a separate 5G CPE presented as Ethernet. Pair B One with the 5G Adapter when the customer wants cellular presented as Ethernet instead of using B One 5G's embedded modem. Use the broader retail branch failover recipe when wired broadband is clearly primary and cellular is only backup.

Do not sell a single-radio design as dual cellular. B One 5G with two SIMs is a good retail answer, but only one embedded cellular modem is active at a time. If the customer expects two cellular paths at once, quote the 5G Dongle as the USB-C second-cellular product, use the 5G Adapter for Ethernet handoff, or step up to BR2 Pro.

## Licensing

**PrimeCare** is assumed for B One 5G. It covers InControl 2, SpeedFusion Hot Failover, Smoothing, Bandwidth Bonding, and the complimentary SpeedFusion Connect usage allocation. Hot Failover is what keeps payment and cloud POS sessions more stable when the active WAN changes.

The 5G Dongle and 5G Adapter should be quoted as products with their own SKU, care-plan, data-plan, SIM/eSIM, antenna, and mounting requirements. Manage the retail WAN policy on the B One 5G or branch router, and treat the 5G product as an added WAN path.

## Accessories / BOM notes

- Carrier-diverse SIMs or eSIMs. Two SIMs from one carrier are account redundancy, not path diversity.
- Remote 5G antennas if the router is in a back office, under a counter, inside a rack, or behind low-E glass.
- 5G Dongle, USB-C cabling, and secure mounting if the B One 5G needs a second active cellular WAN over USB-C.
- 5G Adapter, Ethernet patching, power/PoE planning, and secure mounting if the cellular handoff should be Ethernet.
- PoE switch and APs when the store has more than a small local Wi-Fi footprint.
- Traffic shaping policy that protects POS, payment, and ordering systems ahead of cameras and guest Wi-Fi.

## Known gotchas

- Dual SIM does not mean dual active cellular. A single modem can fail between SIMs, but it cannot use both SIMs as two simultaneous WANs.
- SIM failover can take longer than WAN failover between two active radios. For payment-heavy stores, test the actual application behavior before promising seamless operation.
- Confirm 5G Dongle compatibility and firmware on the exact B One 5G deployment. The router must support USB WAN, and the 5G Dongle consumes that USB-C WAN path.
- Do not quote the USB-C-only 5G Dongle as the cellular product for Balance 310. Balance 310 has no USB WAN; use the 5G Adapter or another Ethernet cellular handoff there.
- 5G Dongle and 5G Adapter are newer products. Confirm exact region SKUs, carrier certifications, and availability from the current price list before quoting.
- Metered or deprioritized 5G plans can look fine in a speed test and still fail under evening retail congestion. Test during business hours.
- Cameras and guest Wi-Fi can burn cellular data quickly. Keep critical business VLANs separate from best-effort traffic.

## Sources

- B One 5G datasheet: https://www.peplink.com/compare/tech-specs/b-one-5g.pdf
- B One 5G product page: https://www.peplink.com/products/soho-routers/b-one-5g/
- 5G Dongle datasheet: https://download.peplink.com/resources/pepwave_5g_dongle_datasheet.pdf
- Peplink resource downloads (5G Adapter and 5G Dongle references): https://www.peplink.com/support/download-datasheet/
- B One datasheet: https://www.peplink.com/compare/tech-specs/b-one.pdf
- BR2 Pro datasheet: https://www.peplink.com/compare/tech-specs/br2-pro.pdf
- Balance 310 datasheet: https://www.peplink.com/compare/tech-specs/balance-310.pdf
- Internal field note, 2026-05-03: 5G Dongle is USB-C only; 5G Adapter is the larger Ethernet-port product.
- Dataset: `data/peplink_all_devices.json` (devices: "B One 5G", "5G Dongle", "5G Adapter", "B One", "BR2 Pro", "Balance 310", last updated 2026-05-03)
