---
name: Remote Industrial SCADA Monitoring
slug: remote-industrial-scada-monitoring
use_cases:
  - scada
  - pump station
  - water utility
  - wastewater
  - utility monitoring
  - pipeline monitoring
  - remote telemetry
  - industrial iot
  - m2m
  - unmanned infrastructure
primary_devices:
  - BR1 Mini 5G
alternate_devices:
  - BR1 Mini
  - BR1 Pro 5G
  - Balance 580X (HW2)
licenses:
  - PrimeCare or BR1 Mini feature pack (for failover and SpeedFusion features where required)
  - CarePlan / SpeedFusion license on central Balance head end when peer count exceeds defaults
  - Virtual WAN Activation License (for separate telemetry, camera, and management overlays)
last_reviewed: 2026-05-03
---

# Remote Industrial SCADA Monitoring

## The scenario

A utility, pipeline operator, water district, or industrial site needs secure connectivity for remote telemetry, PLC/RTU access, pump monitoring, cameras, environmental sensors, and maintenance diagnostics. Sites are geographically dispersed, often have weak cellular coverage, and may only be visited when something breaks. The goal is low-touch, centrally managed, secure connectivity with fewer truck rolls.

## Why this pick

The **BR1 Mini 5G** is the default remote endpoint for new deployments because it is compact, supports 5G, has two SIM slots, and runs from DC 10-30V with low power draw. It provides enough performance for SCADA and camera events while keeping the site hardware inexpensive enough for a many-site rollout.

Use a central **Balance 580X (HW2)** when the customer needs many secure site-to-site tunnels, inbound routing, and centralized policy. It provides up to 8 Gbps router throughput, 1 Gbps SpeedFusion VPN throughput with or without AES, and 500–2000 recommended users. The dataset specifies 100 SpeedFusion peers by default, expandable to 300 or 500 with optional licenses. Verify aggregate tunnel load and head-end sizing for the actual rollout.

**Balance 380** and **Balance 380X** are legacy products. Keep their details for supporting an installed network and planning migration; do not specify them for new sites or as alternate head ends. Peplink lists Balance 580X (HW2) as their replacement candidate. The older Balance 580X HW1 is also legacy, so the hardware revision matters.

## When to step up

- **BR1 Pro 5G** when the remote site also needs GPS, Wi-Fi 6, higher SpeedFusion throughput, GPIO/ignition features, or AP/switch control.
- **BR2 Pro** when serial RS-232, dual 5G modems, four SIMs, or USB WAN are needed at a higher-value site.
- **SDX** or **SDX Pro** at the head end when expansion, interfaces, or tunnel requirements exceed the selected Balance 580X (HW2) configuration. Compare the exact throughput and peer limits rather than assuming every larger chassis is faster.

## When to step down

Use LTE **BR1 Mini** for low-bandwidth fixed telemetry where 5G is not available and cost matters more than headroom. Do not overbuild every pump station with a dual-modem router if the site only sends telemetry and alarm state; save BR2 Pro for the stations with cameras, local operators, or serial/USB requirements.

## Licensing

BR1 Mini 5G requires PrimeCare or the feature pack for Ethernet WAN, Hot Failover, Smoothing, and Bandwidth Bonding. For a private SCADA network, plan the SpeedFusion peer count and encrypted throughput at the head end. Balance 580X (HW2) includes 100 peers; expansion to 300 or 500 requires the optional SFN-LC-300 or SFN-LC-500 license respectively. Verify the required license and compatibility before quoting a larger rollout.

## Accessories / BOM notes

- High-gain external antennas, mounted outside metal pump cabinets.
- Industrial enclosure, surge protection, DIN mounting, and controlled power.
- Dual-carrier SIMs or a managed SIM provider with confirmed rural coverage.
- Optional camera VLAN separated from PLC/RTU traffic.

## Known gotchas

- BR1 Pro 5G has mixed lifecycle status. Before including it in a new solution, select an exact eligible SKU with `query.py skus "BR1 Pro 5G" --new-solutions` and verify the hardware revision. Exclude 5GH/5GD variants; an empty eligible-SKU result does not establish a purchasable option.
- Legacy radio replacement is usually a network-management project, not just a modem swap. Decide addressing, tunnel topology, alarm handling, and remote-access policy up front.
- Weak rural cellular can make a cheaper router look bad. Antenna placement and carrier selection matter more than the router SKU.
- Avoid sending continuous video over metered cellular unless the customer explicitly accepts the data cost.
- Many utilities need static addressing or private APNs. Validate carrier provisioning before staging hardware.

## Sources

- Peplink case study: https://www.peplink.com/case-studies/reliable-water-infrastructure-monitoring-across-county-lines-with-peplink/
- Peplink case study: https://www.peplink.com/case-studies/hyperlink-boosts-scada-performance-with-peplink-in-remote-pipeline-operations/
- Case studies category: https://www.peplink.com/case-studies/smart-construction/
- BR1 Mini 5G datasheet: https://www.peplink.com/compare/tech-specs/br1-mini-5g.pdf
- Balance 580X product page (HW2 record has no datasheet URL in the dataset): https://www.peplink.com/products/enterprise-routers/balance-580x
- Legacy products and replacement guidance (checked 2026-10-09): https://www.peplink.com/legacy-products/
- Dataset: `data/peplink_all_devices.json` (devices: "BR1 Mini 5G", "BR1 Mini", "BR1 Pro 5G", "Balance 580X (HW2)", last updated 2026-10-09)
