# Peplink Device Families

Read this when you need to orient a user who asks about a family rather than a specific SKU (e.g., "what's the difference between HD2 and HD4?" or "what's a Transit?").

These families include multiple hardware generations. Use `query.py list --new-solutions` and verify the exact record/SKU lifecycle before making a new-solution recommendation. Legacy products stay in the catalog for existing-installation support, specification lookups, and migration planning; do not offer them as new equipment or alternates. Family names and case studies do not establish eligibility.

## Routers

- **BR1 series** — Single-modem cellular routers, including compact BR1 Mini models and BR1 Pro 5G. Older BR1 ENT, M2M, Pro, and certain hardware revisions are legacy. BR1 Pro 5G has mixed lifecycle status: 5GH/5GD variants are legacy, so resolve an exact eligible SKU before recommending it.
- **BR2 series** — Two cellular modems, dual-SIM per modem. "BR2 Pro" is the current high-end; "BR2 Micro" is a compact variant. Use when a single BR1 isn't enough but an HD2 MBX is overkill.
- **HD2 / HD4 series** — Mobility routers with two or four modems. MBX variants are distinct from legacy MAX HD2/HD4, Mini, and IP67 products. Match the exact model and revision instead of transferring lifecycle status across the family.
- **Transit series** — Mobility products for transport deployments. Transit, Transit 5G, Transit Duo, Transit Core, and Transit Mini are legacy. Transit Duo Pro and Transit Pro E are distinct models; verify them separately.
- **Balance series** — Stationary enterprise SD-WAN spanning several generations. Balance 380/380X and many older numbered models are legacy. Balance 310 5G HW1–2 and Balance 580X HW1 are legacy, while HW3 and HW2 respectively have separate records. Do not infer performance, integrated cellular, or lifecycle from the number or suffix alone.
- **B One / B One Plus / B One 5G** — Enterprise branch routers. Check the exact model for integrated cellular and WAN interfaces.
- **Dome series** — Outdoor units including HD1 Dome Pro, Dome Pro Duo, and Dome Pro LR. HD1 Dome and HD2 Dome are legacy. Verify environmental ratings and installation requirements on the exact model.
- **IP55 / IP67 variants** — Weather-sealed products; the older BR1 and HD2/HD4 variants are legacy. An ingress-protection rating does not establish new-solution eligibility.
- **SDX, SDX Pro, EPX** — Enterprise SpeedFusion head-ends used to terminate tunnels from fleets of edge routers. EPX is legacy; inspect its suggested replacements for migration planning.
- **UBR series** — UBR LTE and UBR Plus are legacy mobile routers, retained for existing-equipment reference.
- **MAX Adapter** — External cellular connectivity for an existing network. The 5GH variant is legacy; check the exact SKU rather than treating all variants alike.
- **PDX** — Specialized datacenter/head-end unit.
- **SpeedFusion Engine** — A legacy module retained for existing-equipment reference.

## Access Points

The catalog includes AP One and AP Pro products across Wi-Fi generations. The older **AP One Enterprise (HW2)** (Wi-Fi 5) is legacy and must not be confused with the newer **AP One Enterprise** (Wi-Fi 7). **AP One Flex** and older **AP Pro AC/Duo/300M** products are also legacy. Use eligible exact models such as AP One AX, AP One AX Lite, AP One Rugged, or AP Pro AX as candidates, then verify their specifications and environment ratings.

**AP Pro AX Legacy HW2** has conflicting source labels and is marked `review_required`; exclude it from new solutions until resolved. It is distinct from the eligible AP Pro AX record.

## Switches

Two naming conventions coexist in the catalog, with different lifecycle status:

- Descriptive: "8 PoE 10G Switch", "24 PoE 2.5G Switch", "48 PoE 2.5G Switch", "24 PoE 2.5G Switch Rugged".
- Legacy prefixed models: "SD Switch 24-Port Enterprise", "SD Switch 48-Port Enterprise", "SD Switch 8/16/24-Port Rugged". Retain these for support and migration, and exclude them from new-solution BOMs.

The "Rugged" line is DIN-rail or industrial-enclosure-friendly; "Enterprise" is a standard 1U rackmount. Port speed is in the product name (2.5G, 10G).

## Spec layout reminder

- Routers: nine nested sections (Interfaces, Performance, Wireless details, Features, Core Functionality, Advanced QoS Functionality, VPN Functionality, Hardware, Warranty Info).
- APs and Switches: one flat section called `Specifications` with all fields as top-level entries.

Keep this reminder handy when formatting comparison answers — cross-type comparisons will have lots of empty cells, which is expected.
