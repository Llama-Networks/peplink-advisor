#!/usr/bin/env python3
"""Assemble the Anthropic artifacts for Claude hosts.

This build ships two Anthropic-targeted zips because Anthropic currently has
two distinct install formats — both of which Claude Desktop's "Customize"
flow accepts only as `.zip` (the `.plugin` extension is rejected by the
upload handler, see anthropics/claude-code#40414 and #28337):

1. Plugin-bundle zip (what Claude Desktop's Customize → plugin install and
   Claude Code plugin installs expect). `.claude-plugin/plugin.json` sits at
   the zip root:

       .claude-plugin/plugin.json
       skills/peplink-advisor/SKILL.md
       skills/peplink-advisor/{scripts,data,solutions,references}/...

   This is written to `dist/peplink-advisor-anthropic-plugin-<version>.zip`.

2. Agent Skills-format zip (for hosts that still take the single-skill
   layout, e.g. dropping into `~/.claude/skills/` for Claude Code):

       peplink-advisor/
       ├── SKILL.md
       ├── scripts/
       ├── data/
       ├── solutions/
       └── references/

   This is written to `dist/peplink-advisor-anthropic-<version>.zip`.

Run from anywhere:

    python3 build/build_anthropic.py

Safe to re-run; dist/ is rebuilt each time.
"""
from __future__ import annotations

import re
import shutil
import tempfile
import zipfile
from pathlib import Path

from common import repo_root, read_version


SKILL_NAME = "peplink-advisor"
DESKTOP_ARTIFACT_PREFIX = "peplink-advisor-anthropic"
PLUGIN_ARTIFACT_PREFIX = "peplink-advisor-anthropic-plugin"

# Claude Desktop enforces: lowercase letters, numbers, and hyphens, max 64 chars.
NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")


def build_skill_md(core_skill: Path, frontmatter_yaml: Path) -> str:
    """Prepend the Anthropic frontmatter to the portable SKILL body."""
    body = core_skill.read_text().lstrip()
    fm = frontmatter_yaml.read_text().rstrip()
    lines = [ln for ln in fm.splitlines() if not ln.lstrip().startswith("#")]
    while lines and not lines[0].strip():
        lines.pop(0)
    frontmatter = "\n".join(lines).strip()

    name_match = re.search(r"^name:\s*(\S+)\s*$", frontmatter, re.MULTILINE)
    if not name_match:
        raise SystemExit("frontmatter.yaml is missing a `name:` field")
    name = name_match.group(1)
    if name != SKILL_NAME:
        raise SystemExit(
            f"frontmatter name {name!r} must match SKILL_NAME {SKILL_NAME!r} "
            "(Claude Desktop requires the name field to match the top-level "
            "folder inside the zip)"
        )
    if not NAME_RE.match(name):
        raise SystemExit(
            f"frontmatter name {name!r} is not Claude Desktop-compliant — "
            "must be lowercase letters, numbers, and hyphens only, max 64 chars"
        )
    if not re.search(r"^description:", frontmatter, re.MULTILINE):
        raise SystemExit("frontmatter.yaml is missing a `description:` field")

    return f"---\n{frontmatter}\n---\n\n{body}"


def zip_tree(stage: Path, artifact: Path) -> None:
    if artifact.exists():
        artifact.unlink()
    with zipfile.ZipFile(artifact, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(stage.rglob("*")):
            if p.is_file():
                zf.write(p, p.relative_to(stage))


def stage_desktop_skill(root: Path, stage: Path) -> None:
    skill_dir = stage / SKILL_NAME
    skill_dir.mkdir(parents=True)

    skill_md = build_skill_md(
        core_skill=root / "core" / "SKILL.md",
        frontmatter_yaml=root / "adapters" / "anthropic" / "frontmatter.yaml",
    )
    (skill_dir / "SKILL.md").write_text(skill_md)

    for sub in ("scripts", "data", "solutions", "references"):
        src = root / "core" / sub
        if src.exists():
            shutil.copytree(src, skill_dir / sub)


def stage_plugin_bundle(root: Path, stage: Path) -> None:
    plugin_manifest = root / "adapters" / "anthropic" / ".claude-plugin" / "plugin.json"
    (stage / ".claude-plugin").mkdir(parents=True)
    shutil.copy(plugin_manifest, stage / ".claude-plugin" / "plugin.json")

    skill_dir = stage / "skills" / SKILL_NAME
    skill_dir.mkdir(parents=True)

    skill_md = build_skill_md(
        core_skill=root / "core" / "SKILL.md",
        frontmatter_yaml=root / "adapters" / "anthropic" / "frontmatter.yaml",
    )
    (skill_dir / "SKILL.md").write_text(skill_md)

    for sub in ("scripts", "data", "solutions", "references"):
        src = root / "core" / sub
        if src.exists():
            shutil.copytree(src, skill_dir / sub)


def main() -> None:
    root = repo_root()
    version = read_version()
    dist = root / "dist"
    dist.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="peplink-anthropic-") as tmp:
        stage_root = Path(tmp)
        desktop_stage = stage_root / "desktop"
        plugin_stage = stage_root / "plugin"

        stage_desktop_skill(root, desktop_stage)
        stage_plugin_bundle(root, plugin_stage)

        # Clean any previously-built artifacts, including the legacy `.plugin`
        # extension we used before discovering Claude Desktop rejects it.
        for stale in dist.glob(f"{DESKTOP_ARTIFACT_PREFIX}-*.zip"):
            if stale.name.startswith(f"{PLUGIN_ARTIFACT_PREFIX}-"):
                continue
            stale.unlink()
        for stale in dist.glob(f"{PLUGIN_ARTIFACT_PREFIX}-*.zip"):
            stale.unlink()
        for stale in dist.glob(f"{PLUGIN_ARTIFACT_PREFIX}-*.plugin"):
            stale.unlink()

        desktop_artifact = dist / f"{DESKTOP_ARTIFACT_PREFIX}-{version}.zip"
        plugin_artifact = dist / f"{PLUGIN_ARTIFACT_PREFIX}-{version}.zip"
        zip_tree(desktop_stage, desktop_artifact)
        zip_tree(plugin_stage, plugin_artifact)

    desktop_size_kb = desktop_artifact.stat().st_size / 1024
    plugin_size_kb = plugin_artifact.stat().st_size / 1024
    print(f"[anthropic] wrote {desktop_artifact.relative_to(root)} ({desktop_size_kb:.0f} KB)")
    print(f"[anthropic] wrote {plugin_artifact.relative_to(root)} ({plugin_size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
