---
name: Telemedicine Rural Clinic
slug: telemedicine-rural-clinic
use_cases:
  - telemedicine
  - rural clinic
  - mobile clinic
  - healthcare
  - hospital internet
  - vaccine clinic
  - remote healthcare
  - field clinic
  - clinic wifi
  - medical outreach
primary_devices:
  - B One 5G
  - AP One AX
alternate_devices:
  - B One
  - BR2 Pro
  - Balance 310
  - SDX Pro
licenses:
  - PrimeCare (SpeedFusion, InControl, InTouch, and SpeedFusion Connect usage)
  - Virtual WAN Activation License (for clinical, staff, public Wi-Fi, and device networks)
  - AP care / InControl subscription as required for managed Wi-Fi
last_reviewed: 2026-05-03
---

# Telemedicine Rural Clinic

## The scenario

A rural clinic, mobile health unit, vaccine site, or telemedicine program needs stable connectivity for video consults, diagnostic devices, cloud medical apps, staff laptops, and sometimes public or school Wi-Fi nearby. The WAN mix is usually cellular plus satellite, with limited local technical support and a strong need for remote management.

## Why this pick

The **B One 5G** is the default fixed-clinic router when cellular is part of the design. It handles wired or satellite Ethernet WANs alongside one integrated 5G modem with two SIM slots, and it includes 2x2 Wi-Fi 6 for the local clinic footprint. It provides 1 Gbps router throughput, 400 Mbps SpeedFusion VPN throughput unencrypted / 200 Mbps encrypted, 1-150 recommended users, and AP/switch management.

Pair it with **AP One AX** when the clinic or nearby buildings need proper Wi-Fi 6 coverage. AP One AX supports 16 SSIDs and 256 recommended concurrent users per radio, which makes it suitable for separate clinical, staff, device, and public networks.

## When to step up

- **Balance 310** for a larger fixed clinic, regional clinic hub, or site that needs a stronger wired core. It has 2x 2.5GE WAN, 4x 10GE LAN, 4 Gbps router throughput, 1 Gbps encrypted SpeedFusion throughput, and 50-500 recommended users. Add external 5G or satellite CPE if cellular is still part of the WAN design.
- **BR2 Pro** for a mobile clinic or rugged all-in-one unit needing two active 5G modems, four SIM slots, Wi-Fi 6, GPS, USB WAN, or serial.
- **SDX Pro** for a hospital or large clinic hub with many remote sites and high tunnel counts.
- **HD4 MBX 5G** for emergency medical deployments with many concurrent cellular paths and a command-trailer form factor.

## When to step down

Use **B One** for a small clinic that does not need integrated cellular and has wired broadband, Starlink Ethernet, or separate cellular CPE. Do not use a no-Wi-Fi Mini as the clinic router unless APs, switching, and remote management are handled separately.

## Licensing

PrimeCare is assumed for SpeedFusion Hot Failover, Smoothing, Bandwidth Bonding, InControl, InTouch, and SpeedFusion Connect usage. Use Virtual WAN licenses when clinical traffic must stay isolated from public/community Wi-Fi and IoT/medical devices. If PHI-bearing systems traverse the tunnel, confirm encryption, endpoint ownership, and compliance requirements with the healthcare IT owner.

## Accessories / BOM notes

- Long-range cellular antennas or roof antennas when clinics are far from towers.
- Satellite terminal where cellular is weak or unavailable.
- AP One AX for indoor Wi-Fi; outdoor APs or wireless bridges if nearby buildings need coverage.
- UPS, clean shutdown, and spare SIMs for mobile or off-grid clinics.

## Known gotchas

- Public Wi-Fi and telemedicine cannot share an unconstrained flat LAN. Segment and rate-limit public access.
- Clinical devices may require static addressing, allow lists, or VPN policies. Collect those requirements before staging.
- If satellite is the only high-bandwidth WAN, test real video-call latency and jitter instead of relying on speed tests.
- Remote clinics need a support model. InControl access, labeling, and a local reboot procedure reduce avoidable dispatches.

## Sources

- Peplink case study: https://www.peplink.com/case-studies/telemedicine-extends-its-care-to-remote-communities-with-peplink/
- Case studies category: https://www.peplink.com/case-studies/telemedicine/
- B One 5G datasheet: https://www.peplink.com/compare/tech-specs/b-one-5g.pdf
- B One datasheet: https://www.peplink.com/compare/tech-specs/b-one.pdf
- Balance 310 datasheet: https://www.peplink.com/compare/tech-specs/balance-310.pdf
- AP One AX datasheet: https://download.peplink.com/resources/pepwave_ap_one_ax_datasheet.pdf
- BR2 Pro datasheet: https://www.peplink.com/compare/tech-specs/br2-pro.pdf
- Dataset: `data/peplink_all_devices.json` (devices: "B One 5G", "B One", "AP One AX", "BR2 Pro", "Balance 310", last updated 2026-05-03)
