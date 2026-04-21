#!/usr/bin/env python3
"""Assemble the Anthropic (Claude Code / Cowork) plugin artifact.

Layout produced inside dist/peplink-advisor-<version>.plugin (a zip):

    .claude-plugin/plugin.json
    skills/peplink-advisor/SKILL.md        (frontmatter + core SKILL body)
    skills/peplink-advisor/scripts/        (core/scripts/*)
    skills/peplink-advisor/data/           (core/data/*)
    skills/peplink-advisor/solutions/      (core/solutions/*)
    skills/peplink-advisor/references/     (core/references/*)

Run from anywhere:

    python3 build/build_anthropic.py

Safe to re-run; dist/ is rebuilt each time.
"""
from __future__ import annotations
import shutil
import tempfile
import zipfile
from pathlib import Path

from common import repo_root, read_version


SKILL_NAME = "peplink-advisor"


def build_skill_md(core_skill: Path, frontmatter_yaml: Path) -> str:
    """Prepend the Anthropic frontmatter to the portable SKILL body."""
    body = core_skill.read_text().lstrip()
    fm = frontmatter_yaml.read_text().rstrip()
    # Strip comment lines from frontmatter.yaml before wrapping in `---` fences.
    lines = [ln for ln in fm.splitlines() if not ln.lstrip().startswith("#")]
    # Remove any leading blank lines after comment stripping.
    while lines and not lines[0].strip():
        lines.pop(0)
    frontmatter = "\n".join(lines).strip()
    return f"---\n{frontmatter}\n---\n\n{body}"


def main() -> None:
    root = repo_root()
    version = read_version()
    dist = root / "dist"
    dist.mkdir(exist_ok=True)

    # Stage in a tempdir rather than under dist/ — keeps the build insensitive
    # to mount/permission quirks in sandboxed environments and means a failed
    # build never leaves cruft in the repo working tree.
    with tempfile.TemporaryDirectory(prefix="peplink-anthropic-") as tmp:
        stage = Path(tmp)

        # .claude-plugin/plugin.json
        plugin_json_src = root / "adapters" / "anthropic" / ".claude-plugin" / "plugin.json"
        (stage / ".claude-plugin").mkdir(parents=True)
        shutil.copy(plugin_json_src, stage / ".claude-plugin" / "plugin.json")

        # skills/<name>/SKILL.md with injected frontmatter
        skill_dir = stage / "skills" / SKILL_NAME
        skill_dir.mkdir(parents=True)
        skill_md = build_skill_md(
            core_skill=root / "core" / "SKILL.md",
            frontmatter_yaml=root / "adapters" / "anthropic" / "frontmatter.yaml",
        )
        (skill_dir / "SKILL.md").write_text(skill_md)

        # Copy the portable bundles verbatim.
        for sub in ("scripts", "data", "solutions", "references"):
            src = root / "core" / sub
            if src.exists():
                shutil.copytree(src, skill_dir / sub)

        # Zip it up into a .plugin file.
        artifact = dist / f"{SKILL_NAME}-{version}.plugin"
        if artifact.exists():
            artifact.unlink()
        with zipfile.ZipFile(artifact, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in sorted(stage.rglob("*")):
                if p.is_file():
                    zf.write(p, p.relative_to(stage))

    size_kb = artifact.stat().st_size / 1024
    print(f"[anthropic] wrote {artifact.relative_to(root)} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
