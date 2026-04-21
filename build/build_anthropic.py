#!/usr/bin/env python3
"""Assemble the Anthropic skill artifact for Claude Desktop / claude.ai.

Claude Desktop's "Upload skill" flow expects a .zip whose root is a single
folder named after the skill, with SKILL.md at the top of that folder. This
is the Agent Skills open-standard layout — see
https://support.claude.com/en/articles/12512198-how-to-create-custom-skills

Layout produced inside dist/peplink-advisor-anthropic-<version>.zip:

    peplink-advisor/
    ├── SKILL.md                (frontmatter + core SKILL body)
    ├── scripts/                (core/scripts/*)
    ├── data/                   (core/data/*)
    ├── solutions/              (core/solutions/*)
    └── references/             (core/references/*)

Run from anywhere:

    python3 build/build_anthropic.py

Safe to re-run; dist/ is rebuilt each time.

Note: This artifact also works as a personal skill in Claude Code — unzip it
into ~/.claude/skills/ and the skill is discovered automatically.
"""
from __future__ import annotations
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

from common import repo_root, read_version


SKILL_NAME = "peplink-advisor"
ARTIFACT_PREFIX = "peplink-advisor-anthropic"

# Claude Desktop enforces: lowercase letters, numbers, and hyphens, max 64 chars.
NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")


def build_skill_md(core_skill: Path, frontmatter_yaml: Path) -> str:
    """Prepend the Anthropic frontmatter to the portable SKILL body.

    The frontmatter must include `name` and `description` for Claude Desktop to
    accept the upload. `name` must match the top-level folder name in the zip.
    """
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


def main() -> None:
    root = repo_root()
    version = read_version()
    dist = root / "dist"
    dist.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="peplink-anthropic-") as tmp:
        stage = Path(tmp)
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

        # Remove any stale .plugin artifact from previous builds so releases
        # don't accidentally ship both formats.
        for stale in dist.glob(f"{ARTIFACT_PREFIX}-*.plugin"):
            stale.unlink()

        artifact = dist / f"{ARTIFACT_PREFIX}-{version}.zip"
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
