"""Shared helpers for the adapter build scripts.

Both build scripts need to find the repo root, read the version, and read the
dataset's "last updated" date. Keep that logic here so the two builds stay in
sync.
"""
from __future__ import annotations
import json
import os
import re
from pathlib import Path


def repo_root() -> Path:
    """Return the repository root (the directory containing core/ and adapters/)."""
    here = Path(__file__).resolve().parent
    # build/ is at the repo root
    return here.parent


def read_version() -> str:
    """Version comes from the Anthropic plugin.json — that's the single source of truth."""
    pj = repo_root() / "adapters" / "anthropic" / ".claude-plugin" / "plugin.json"
    return json.loads(pj.read_text())["version"]


def read_dataset_date() -> str:
    """Pull the 'Dataset last updated' line out of core/SKILL.md."""
    skill = (repo_root() / "core" / "SKILL.md").read_text()
    m = re.search(r"Dataset last updated:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", skill)
    return m.group(1) if m else "unknown"


def iter_manifest(path: Path):
    """Yield (src_path, dest_name) tuples from a knowledge-manifest.txt."""
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "->" in line:
            src, dest = [s.strip() for s in line.split("->", 1)]
        else:
            src = dest = line
        yield src, dest
