#!/usr/bin/env python3
"""Validate the built ChatGPT bundle before release."""
from __future__ import annotations

import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

from common import repo_root, read_version


REQUIRED_FILES = (
    "instructions.md",
    "config.json",
    "README-deploy.md",
    "knowledge/query.py",
    "knowledge/peplink_all_devices.json",
)

STALE_INSTRUCTION_SNIPPETS = (
    "python3 scripts/query.py",
    "`data/peplink_all_devices.json`",
    "`ls solutions/`",
    "draft a new solution file",
    "turning the answer into a Cowork artifact",
)


def main() -> None:
    root = repo_root()
    version = read_version()
    artifact = root / "dist" / f"peplink-advisor-chatgpt-{version}.zip"
    if not artifact.exists():
        raise SystemExit(f"Missing artifact: {artifact}")

    with tempfile.TemporaryDirectory(prefix="verify-peplink-chatgpt-") as tmp:
        stage = Path(tmp)
        with zipfile.ZipFile(artifact) as zf:
            zf.extractall(stage)

        for rel_path in REQUIRED_FILES:
            path = stage / rel_path
            if not path.exists():
                raise SystemExit(f"Bundle is missing required file: {rel_path}")

        instructions = (stage / "instructions.md").read_text()
        for snippet in STALE_INSTRUCTION_SNIPPETS:
            if snippet in instructions:
                raise SystemExit(f"Bundle instructions still contain stale guidance: {snippet}")

        result = subprocess.run(
            ["python3", "query.py", "show", "B One 5G"],
            cwd=stage / "knowledge",
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        if payload.get("product_name") != "B One 5G":
            raise SystemExit("Packaged query.py returned an unexpected payload.")

        result = subprocess.run(
            ["python3", "query.py", "skus", "B One 5G"],
            cwd=stage / "knowledge",
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        if not payload.get("sku_variants"):
            raise SystemExit("Packaged query.py did not return SKU variants.")

    print(f"[chatgpt] verified {artifact.relative_to(root)}")


if __name__ == "__main__":
    main()
