# Changelog

All notable changes to Peplink Advisor are documented here. This project follows [Semantic Versioning](https://semver.org/) — breaking changes to the SKILL contract, solutions schema, or dataset shape bump MINOR until 1.0.

## [Unreleased]

### Fixed
- Anthropic releases now ship both official packaging formats: the Claude Desktop / claude.ai skill zip and a Cowork / Claude Code plugin bundle that includes `.claude-plugin/plugin.json`.
- CI and release workflows now verify both Anthropic artifacts before publishing them.

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
