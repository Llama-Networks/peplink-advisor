#!/usr/bin/env python3
"""Validate the built Anthropic artifacts before release."""
from __future__ import annotations

import json
import tempfile
import zipfile
from pathlib import Path

from common import repo_root, read_version


def require(path: Path, rel_path: str) -> None:
    if not path.exists():
        raise SystemExit(f"Bundle is missing required file: {rel_path}")


def main() -> None:
    root = repo_root()
    version = read_version()
    dist = root / "dist"
    desktop_artifact = dist / f"peplink-advisor-anthropic-{version}.zip"
    plugin_artifact = dist / f"peplink-advisor-anthropic-plugin-{version}.zip"

    for artifact in (desktop_artifact, plugin_artifact):
        if not artifact.exists():
            raise SystemExit(f"Missing artifact: {artifact}")

    with tempfile.TemporaryDirectory(prefix="verify-peplink-anthropic-") as tmp:
        stage = Path(tmp)

        desktop_dir = stage / "desktop"
        with zipfile.ZipFile(desktop_artifact) as zf:
            zf.extractall(desktop_dir)
        require(desktop_dir / "peplink-advisor" / "SKILL.md", "peplink-advisor/SKILL.md")
        if (desktop_dir / ".claude-plugin" / "plugin.json").exists():
            raise SystemExit("Desktop skill zip should not contain .claude-plugin/plugin.json")

        plugin_dir = stage / "plugin"
        with zipfile.ZipFile(plugin_artifact) as zf:
            zf.extractall(plugin_dir)
        require(plugin_dir / ".claude-plugin" / "plugin.json", ".claude-plugin/plugin.json")
        require(plugin_dir / "skills" / "peplink-advisor" / "SKILL.md", "skills/peplink-advisor/SKILL.md")

        plugin_manifest = json.loads((plugin_dir / ".claude-plugin" / "plugin.json").read_text())
        if plugin_manifest.get("name") != "peplink-advisor":
            raise SystemExit("Plugin manifest name is not peplink-advisor")

    print(f"[anthropic] verified {desktop_artifact.relative_to(root)}")
    print(f"[anthropic] verified {plugin_artifact.relative_to(root)}")


if __name__ == "__main__":
    main()
