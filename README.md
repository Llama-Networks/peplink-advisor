# Peplink Advisor

Peplink Advisor is a downloadable AI assistant package for people who need to specify Peplink hardware, licenses, and related accessories. It answers Peplink product questions using a bundled catalog instead of relying on memory.

Use it to:

- Look up device specs and caveats.
- Compare routers, access points, switches, and modules.
- Shortlist hardware for branch, marine, vehicle, retail, IoT, and bonded cellular deployments.
- Check product SKUs and compatible add-ons, including care plans, licenses, modules, SIM injectors, antennas, and accessories.
- Keep licensing notes visible when features depend on PrimeCare, SpeedFusion, Virtual WAN, eSIM, or other add-ons.

This project is not affiliated with, endorsed by, or sponsored by Peplink. Peplink's own product pages, datasheets, partner portal, and price lists remain authoritative.

## Download

Most users should download a release from the [GitHub Releases page](../../releases). Each release includes ready-to-use packages:

- `peplink-advisor-anthropic-plugin-<version>.zip` for Claude Desktop and Claude Code plugin installs.
- `peplink-advisor-anthropic-standalone-<version>.zip` for users who want a standalone Claude skill folder.
- `peplink-advisor-chatgpt-<version>.zip` for creating or updating a ChatGPT Custom GPT with the included knowledge bundle.

You can also download the repository source if you want to inspect the dataset, run the local query helper, or customize the assistant instructions before packaging it yourself.

## Install

### Claude Desktop

Download `peplink-advisor-anthropic-plugin-<version>.zip`. In Claude Desktop, open Customize and upload the zip. Claude Desktop expects a `.zip` file with a `.claude-plugin/plugin.json` manifest at the root, which this package includes.

### Claude Code

Use the same `peplink-advisor-anthropic-plugin-<version>.zip` with `/plugin install`, or point Claude Code at the unpacked plugin directory.

### Standalone Claude Skill

Download `peplink-advisor-anthropic-standalone-<version>.zip` and unzip it so the skill folder lives at:

```text
~/.claude/skills/peplink-advisor/SKILL.md
```

### ChatGPT Custom GPT

Download `peplink-advisor-chatgpt-<version>.zip`, unzip it, and follow the `README-deploy.md` included in that package. It contains the instructions, configuration, dataset, query helper, and knowledge files needed by the Custom GPT builder.

## What Is Included

The shared source lives under `core/`:

- `core/SKILL.md` contains the assistant instructions.
- `core/data/peplink_all_devices.json` contains the bundled catalog.
- `core/scripts/query.py` returns small, targeted JSON slices from the catalog.
- `core/solutions/` contains curated deployment recipes.
- `core/references/` contains supporting reference notes.

The current catalog contains 165 records: 105 fully specified devices plus SKU-only records for modules, FusionHub licenses, SIM injectors, antennas, and accessories. Many fully specified devices include direct datasheet URLs in addition to product page URLs.

## Example Questions

Ask questions like:

- Which Peplink routers support 5G and GPS?
- Compare the HD2 MBX 5G and HD4 MBX 5G on throughput, cellular count, and VPN performance.
- What SKUs and add-ons apply to the B One 5G?
- Does this feature require PrimeCare or an extra license?
- What would you specify for a retail branch with wired internet plus cellular failover?
- What is a reasonable Peplink hardware stack for a small vessel with guest Wi-Fi?

The advisor is designed to say when the dataset does not contain an answer rather than inventing numbers.

## Optional Local Queries

If you download the source repository, you can query the catalog directly:

```bash
python3 core/scripts/query.py list
python3 core/scripts/query.py show "B One 5G"
python3 core/scripts/query.py compare "HD2 MBX 5G" "HD4 MBX 5G"
python3 core/scripts/query.py filter --type router --field "5G support" --value Yes
python3 core/scripts/query.py skus "B One 5G"
python3 core/scripts/query.py skus --find "LIC-VWAN" --type router
```

The helper prints JSON so you can inspect it directly or pipe it into other tools.

## Custom Defaults

Organizations can add local recommendation preferences in `core/SKILL.md` under `## User-specific instructions`. Examples include preferring global cellular variants, avoiding end-of-sale hardware, or requiring a certain accessory standard.

After changing instructions or data, rebuild the package for the platform you use.

## Data Limits

The bundled dataset is derived from publicly published Peplink specifications and SKU material. It is intended for compatibility, planning, and proposal support. It does not include live inventory, current pricing, distributor availability, private partner terms, or carrier certification status unless that information appears in the bundled source material.

Before committing a customer design or quote, verify important specs against the linked Peplink datasheet or product page and confirm commercial details through your normal supplier or partner channel.

## Contributing

Corrections and deployment recipes are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the kind of source evidence and detail that make updates useful.

## License

MIT. See [LICENSE](LICENSE).
