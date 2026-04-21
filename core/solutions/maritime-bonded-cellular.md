---
name: Maritime Bonded Cellular
slug: maritime-bonded-cellular
use_cases:
  - maritime
  - vessel
  - boat
  - yacht
  - fishing charter
  - ferry
  - coastal
  - offshore
primary_devices:
  - HD2 MBX 5G
alternate_devices:
  - HD4 MBX 5G
  - HD2 Dome
licenses:
  - PrimeCare (SpeedFusion bonding + 500 GB/yr SpeedFusion Connect complimentary)
  - Virtual WAN Activation License (if additional virtual WAN endpoints are needed beyond the 1 included)
last_reviewed: 2026-04-17
---

# Maritime Bonded Cellular

## The scenario

A vessel operating within coastal cellular coverage (charter fishing, day ferry, small cruise, research) needs robust connectivity for crew operations, guest Wi-Fi, and occasional video. Two or more cellular carriers are available in the operating area, and the boat can accommodate exterior antennas. Latency matters less than resilience and continuous uptime as the boat moves between coverage cells.

## Why this pick

The **HD2 MBX 5G** is the default because it pairs two integrated 5G modems with four SIM slots and GPS in a ruggedized chassis. Router throughput is 2.5 Gbps and SpeedFusion VPN throughput is 600 Mbps unencrypted / 500 Mbps with 256-bit AES — well above what cellular can deliver even in ideal conditions, so the router is never the bottleneck. It supports 50–500 recommended users, which comfortably covers crew plus paying passengers on a typical charter. RemoteSIM and FusionSIM are standard, which is important for multi-SIM pools when the vessel crosses regional carrier boundaries.

## When to step up

Go to the **HD4 MBX 5G** when:

- The deployment needs 4 concurrent cellular paths (e.g., near-continuous operation in a low-coverage area where bonding any two carriers still isn't enough).
- The customer wants both a local-SIM and a roaming-SIM tier active on each side, which eats through 2 modems fast.
- The vessel needs additional antenna diversity across the bow/stern.

## When to step down

For a very small vessel or owner-operator with 1–10 users, a **BR1 Pro 5G** or **BR2 Pro** is usually right-sized and far cheaper. You lose the second integrated modem, but you keep SpeedFusion and GPS. Don't step down past a BR1 Pro for a "maritime" use case — the modem count and antenna diversity are what make bonded cellular actually resilient on the water.

For a **permanent fixed installation on a stationary vessel** (houseboat, moored charter boat) consider the **HD2 Dome** — it's an IP67 external unit with 2 modems, simpler to install, but rated for fixed deployment.

## Licensing

- **PrimeCare** is the central license. First year is complimentary on all MBX hardware, and it covers SpeedFusion Hot Failover, Smoothing, Bandwidth Bonding, and 500 GB/yr of complimentary SpeedFusion Connect (their hosted VPN endpoint). Without PrimeCare after year one, the bonding features stop.
- **Virtual WAN**: 1 Virtual WAN is included with active PrimeCare. If the customer wants multiple overlays (crew network vs. guest network vs. shoreside backhaul), they'll need Virtual WAN Activation Licenses for up to 3 total.
- **eSIM**: HW4+ units support Peplink eSIM Data Plans and BYO eSIM, but require firmware 8.3+ / 8.4+ respectively. Verify the hardware revision on the quote before committing.

## Accessories / BOM notes

- External marine-rated cellular antennas (Peplink Puma or 3rd-party Maritime GPS/LTE/5G). Transmit gain matters more than receive gain on a moving vessel.
- Ruggedized DC power (the MBX is DC-capable; check the customer's house battery voltage).
- SIMs: plan for 4 — two per-carrier for primary, two for roaming or a secondary region. FusionSIM can pool them across the fleet if the customer operates multiple boats.

## Known gotchas

- The throughput figures (2.5 Gbps / 600 Mbps / 500 Mbps) are per the latest hardware revision at frame sizes of 1280/1518 bytes. Earlier HW revisions and smaller frames will deliver less. Quote "up to" numbers, not floors.
- Wi-Fi on the HD2 MBX 5G is **2x2 Wi-Fi 5**, not Wi-Fi 6. For guest Wi-Fi on a larger vessel, pair it with an **AP Pro AX** or **AP One AX** outdoor/ruggedized AP rather than relying on the onboard radio.
- Peplink eSIM plans only cover certain regions; confirm coverage for the operating area before selling it as a primary path.

## Sources

- Datasheet (PDF): https://www.peplink.com/compare/tech-specs/hd2-mbx-5g.pdf
- Product page: https://www.peplink.com/products/enterprise-mobility/mbx/
- Dataset: `data/peplink_all_devices.json` (device: "HD2 MBX 5G", last updated 2026-04-17)
