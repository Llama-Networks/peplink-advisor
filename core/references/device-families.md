# Peplink Device Families

Read this when you need to orient a user who asks about a family rather than a specific SKU (e.g., "what's the difference between HD2 and HD4?" or "what's a Transit?").

## Routers

- **BR1 series** — Single-modem cellular routers. Form factors range from tiny IoT ("BR1 Mini", "BR1 Mini M2M") up through prosumer ("BR1 Pro 5G", "BR1 ENT"). Default answer for a small vehicle, kiosk, or single-user mobile setup.
- **BR2 series** — Two cellular modems, dual-SIM per modem. "BR2 Pro" is the current high-end; "BR2 Micro" is a compact variant. Use when a single BR1 isn't enough but an HD2 MBX is overkill.
- **HD2 / HD4 series** — Enterprise Mobility flagship. Two or four integrated modems, ruggedized, GPS. MBX variants (HD2 MBX, HD4 MBX, HD2 MBX 5G, HD4 MBX 5G) are the modern line. MediaFast variants add content caching. The "EC" suffix means higher-capacity edge compute tier.
- **Transit series** — Mid-tier mobility. "Transit", "Transit Duo", "Transit Pro E" — good for fleet vehicles, buses, emergency response where HD2 MBX is too much.
- **Balance series** — Stationary enterprise SD-WAN. Numbered by tier: 20, 20X, 30, 210, 310, 310X, 380, 580, 710, 1350, 2500, 5000. Higher number = more throughput, more WAN ports, more users. "X" suffix indicates cellular-capable; "EC" is the edge-compute variant.
- **B One / B One Plus / B One 5G** — "Enterprise Branch" line, positioned below Balance 30. Good modern entry point for a single branch with integrated cellular.
- **Dome series** — Outdoor IP67 units designed for permanent mount (on a pole, vehicle roof, etc.). HD1 Dome, HD2 Dome, Dome Pro, Dome Pro Duo, Dome Pro LR (long range).
- **IP55 / IP67 variants** — Weather-sealed versions of BR1 and HD2/4. Used for outdoor/harsh-environment deployments.
- **SDX, SDX Pro, EPX** — Datacenter-class SpeedFusion head-ends. These terminate tunnels from fleets of edge routers. Customer is usually a service provider or large enterprise.
- **UBR series** — Ultra-broadband routers. UBR LTE and UBR Plus. Positioned between BR1 and Transit for mobile deployments with a cleaner form factor.
- **MAX Adapter** — Technically a router but really a "drop-in cellular" device that adds bonded cellular to an existing network without replacing the primary router.
- **PDX** — Specialized datacenter/head-end unit.
- **SpeedFusion Engine** — A module rather than a standalone router.

## Access Points

Six current models: **AP One Mini**, **AP One Rugged**, **AP Pro AX**, **AP One Enterprise (HW2)**, **AP One AX**, **AP One AX Lite**. "AX" suffix means Wi-Fi 6. The "Rugged" / outdoor models are IP-rated for outdoor deployment.

## Switches

Nine current models. Two naming conventions coexist:

- Descriptive: "8 PoE 10G Switch", "24 PoE 2.5G Switch", "48 PoE 2.5G Switch", "24 PoE 2.5G Switch Rugged".
- Prefixed: "SD Switch 24-Port Enterprise", "SD Switch 48-Port Enterprise", "SD Switch 8/16/24-Port Rugged".

The "Rugged" line is DIN-rail or industrial-enclosure-friendly; "Enterprise" is a standard 1U rackmount. Port speed is in the product name (2.5G, 10G).

## Spec layout reminder

- Routers: nine nested sections (Interfaces, Performance, Wireless details, Features, Core Functionality, Advanced QoS Functionality, VPN Functionality, Hardware, Warranty Info).
- APs and Switches: one flat section called `Specifications` with all fields as top-level entries.

Keep this reminder handy when formatting comparison answers — cross-type comparisons will have lots of empty cells, which is expected.
