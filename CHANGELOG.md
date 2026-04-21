# Changelog

All notable changes to Peplink Advisor are documented here. This project follows [Semantic Versioning](https://semver.org/) — breaking changes to the SKILL contract, solutions schema, or dataset shape bump MINOR until 1.0.

## [Unreleased]

### Added
- Monorepo layout with `core/` + `adapters/{anthropic,chatgpt}/` + `build/` for dual-platform releases.
- GitHub Actions CI that builds both adapters on every push.
- GitHub Actions release workflow that attaches `.plugin` and `.zip` artifacts to every `v*` tag.

## [0.1.0] — 2026-04-21

### Added
- Initial skill: SKILL.md body, `query.py` helper (list/show/fields/filter/compare/search), `enrich_datasheets.py` maintenance script.
- Dataset of 103 Peplink devices (last updated 2026-04-17), with 84 devices enriched with direct Datasheet URLs.
- Two seed solutions: `retail-branch-cellular-failover` (Balance 20X) and `maritime-bonded-cellular` (HD2 MBX 5G).
- Reference material: `device-families.md`.
- Anthropic plugin artifact (v0.1.0).
- ChatGPT Custom GPT bundle (v0.1.0).
