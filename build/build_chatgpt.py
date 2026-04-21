#!/usr/bin/env python3
"""Assemble the ChatGPT Custom GPT deployment bundle.

Layout produced inside dist/peplink-advisor-chatgpt-<version>.zip:

    instructions.md            — paste into the Custom GPT Instructions field
    config.json                — the name/description/capabilities to apply
    README-deploy.md           — step-by-step for the human configuring the GPT
    knowledge/                 — every file here uploads into GPT Knowledge
        query.py
        peplink_all_devices.json
        solutions/*.md
        references/*.md

Run from anywhere:

    python3 build/build_chatgpt.py

Safe to re-run; dist/ is rebuilt each time.
"""
from __future__ import annotations
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

from common import repo_root, read_version, read_dataset_date, iter_manifest


ARTIFACT_PREFIX = "peplink-advisor-chatgpt"

# Match HTML comment blocks (including multi-line). The template uses them to
# document itself — strip them from the rendered output so only the prompt
# itself lands in ChatGPT's Instructions field.
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def render_instructions(template: str, skill_body: str, dataset_date: str) -> str:
    # Strip documentation comments BEFORE substitution, otherwise placeholders
    # that appear inside a comment (as documentation) would be substituted and
    # then the comment would get closed in the wrong place.
    rendered = HTML_COMMENT.sub("", template)
    rendered = (
        rendered
        .replace("{{SKILL_BODY}}", skill_body.strip())
        .replace("{{DATASET_DATE}}", dataset_date)
        .replace("{{DATASET_PATH}}", "/mnt/data/peplink_all_devices.json")
    )
    # Collapse the 2-3 blank lines left behind by stripped comments.
    rendered = re.sub(r"\n{3,}", "\n\n", rendered)
    return rendered.strip() + "\n"


def main() -> None:
    root = repo_root()
    version = read_version()
    dist = root / "dist"
    dist.mkdir(exist_ok=True)

    # Stage in a tempdir rather than under dist/ — keeps the build insensitive
    # to mount/permission quirks in sandboxed environments.
    with tempfile.TemporaryDirectory(prefix="peplink-chatgpt-") as tmp:
        stage = Path(tmp)
        (stage / "knowledge").mkdir(parents=True)

        # Instructions (rendered from template)
        template = (root / "adapters" / "chatgpt" / "instructions.template.md").read_text()
        skill_body = (root / "core" / "SKILL.md").read_text()
        instructions = render_instructions(template, skill_body, read_dataset_date())
        (stage / "instructions.md").write_text(instructions)

        # Config + deploy README verbatim
        shutil.copy(root / "adapters" / "chatgpt" / "config.json", stage / "config.json")
        shutil.copy(root / "adapters" / "chatgpt" / "README-deploy.md", stage / "README-deploy.md")

        # Knowledge files, renamed per manifest
        manifest_path = root / "adapters" / "chatgpt" / "knowledge-manifest.txt"
        n_bundled = 0
        for src_rel, dest_rel in iter_manifest(manifest_path):
            src = root / src_rel
            dest = stage / "knowledge" / dest_rel
            if not src.exists():
                raise SystemExit(f"knowledge-manifest.txt references missing file: {src_rel}")
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dest)
            n_bundled += 1

        artifact = dist / f"{ARTIFACT_PREFIX}-{version}.zip"
        if artifact.exists():
            artifact.unlink()
        with zipfile.ZipFile(artifact, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in sorted(stage.rglob("*")):
                if p.is_file():
                    zf.write(p, p.relative_to(stage))

    size_kb = artifact.stat().st_size / 1024
    print(f"[chatgpt] wrote {artifact.relative_to(root)} ({size_kb:.0f} KB, {n_bundled} knowledge files)")


if __name__ == "__main__":
    main()
