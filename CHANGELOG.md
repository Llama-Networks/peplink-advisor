# Changelog

All notable changes to Peplink Advisor are documented here. This project follows [Semantic Versioning](https://semver.org/) — breaking changes to the SKILL contract, solutions schema, or dataset shape bump MINOR until 1.0.

## [Unreleased]

## [0.2.2] — 2026-05-03

### Fixed
- Aligned the SKU compatibility catalog with the expanded `productSKU_addonSKUs_with_care.csv` source: all 298 source rows are now represented, including 72 newly mapped variants on existing catalog records and 23 additional SKU-only records for source rows without full device records.

## [0.2.1] — 2026-05-03

### Fixed
- Corrected SKU add-on categorization from the updated source CSV so standard care plans (`SVL-*` / `PRM-*`) are listed under `std*`, plus/enhanced care plans (`ECP-*` / `PCP-*`) are listed under `plus*`, and BR1 Mini bundle SKUs are no longer misclassified as care plans.

## [0.2.0] — 2026-05-03

### Added
- Replaced the device-only catalog with a SKU-enriched catalog covering 165 records, including SKU variants and compatible add-on categories.
- Added `query.py skus` plus SKU-aware search/list behavior so the skill can answer product SKU and add-on compatibility questions.
- Added first-class catalog records for `5G Dongle` and `5G Adapter`, including known SKUs and the USB-C vs. Ethernet handoff distinction.
- Expanded the solutions library with case-study-grounded recipes for public safety, transport Wi-Fi, event internet, broadcast vehicles, remote industrial sites, mining/construction, agriculture, telemedicine, Starlink failover, quick-service restaurants, and retail 5G-primary designs.

### Changed
- Updated skill, Custom GPT, and maintainer documentation for SKU-only catalog records and expanded product types.
- Rewrote public README and contribution guidance for external users, with maintainer workflow notes moved to an ignored local file.
- Updated retail guidance to avoid end-of-sale Balance 20X references, defaulting cellular retail designs to B One 5G / B One and using Balance 310 as the larger branch-core upgrade.

## [0.1.7] — 2026-04-22

### Fixed
- Clarified the `Module Expansion` field on MBX-family devices so `Yes` now explicitly means the cellular radio modules are upgradeable/swappable and that these units do not support FlexModules.

## [0.1.6] — 2026-04-21

### Added
- `core/SKILL.md` now includes a `User-specific instructions` section with precedence guidance and an explicit insertion marker for account-specific defaults.
- `README.md` now points maintainers to the exact place in `core/SKILL.md` where user- or account-specific instructions should be added.

### Fixed
- Plugin-bundle artifact now ships as `peplink-advisor-anthropic-plugin-<version>.zip` (previously `.plugin`). Claude Desktop's Customize upload handler rejects every extension other than `.zip` (anthropics/claude-code#40414, #28337), so the old `.plugin` file failed with "unable to install" and the skill-only `.zip` failed with "missing `.claude-plugin/plugin.json`". The renamed plugin-bundle zip satisfies both requirements in one artifact.
- Anthropic releases still ship the single-skill zip alongside the plugin-bundle zip for hosts that expect the `~/.claude/skills/`-style layout.
- CI and release workflows now verify both Anthropic artifacts before publishing them.

### Changed
- Single-skill zip renamed from `peplink-advisor-anthropic-<version>.zip` to `peplink-advisor-anthropic-standalone-<version>.zip` so the filename makes clear it's for the standalone `~/.claude/skills/` drop-in flow, not the Claude Desktop Customize menu (which needs the plugin-bundle zip).

## [0.1.3] — 2026-04-21

### Fixed
- Anthropic artifact now ships as a Claude Desktop-compliant skill zip (`peplink-advisor-anthropic-<version>.zip`) with a single top-level `peplink-advisor/` folder containing `SKILL.md` at its root. Previous `.plugin`-wrapped builds with a `.claude-plugin/plugin.json` + nested `skills/<name>/` layout were rejected by Claude Desktop's "Upload skill" flow with an "upload failed" error; the new layout matches the [Agent Skills open standard](https://agentskills.io) and the format documented for [custom skills in Claude](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills). The same zip also drops into `~/.claude/skills/` for Claude Code.
- Build now validates that the skill `name` is lowercase letters/numbers/hyphens only and matches the top-level folder in the zip, since Claude Desktop rejects uploads that violate either rule.

## [0.1.1] — 2026-04-21

### Fixed
- ChatGPT bundle path mismatches that made the packaged `query.py` fail to find `peplink_all_devices.json`.
- ChatGPT instructions now strip Anthropic-only guidance and rewrite shared path references to match the shipped GPT knowledge bundle.
- ChatGPT deploy metadata now matches the current GPT editor capability names and no longer points at a stale model setting.
- CI and release workflows now verify the built ChatGPT bundle before shipping artifacts.

## [0.1.0] — 2026-04-21

### Added
- Initial skill: SKILL.md body, `query.py` helper (list/show/fields/filter/compare/search), `enrich_datasheets.py` maintenance script.
- Dataset of 103 Peplink devices (last updated 2026-04-17), with 84 devices enriched with direct Datasheet URLs.
- Two seed solutions: `retail-branch-cellular-failover` (Balance 20X) and `maritime-bonded-cellular` (HD2 MBX 5G).
- Reference material: `device-families.md`.
- Anthropic plugin artifact (v0.1.0).
- ChatGPT Custom GPT bundle (v0.1.0).
