#!/usr/bin/env python3
"""Prevent a release run from replacing assets built from a different commit."""
from __future__ import annotations

import os
import subprocess


def verify_release_tag(tag_name: str, expected_sha: str) -> None:
    if not tag_name or not expected_sha:
        raise SystemExit("RELEASE_TAG and RELEASE_SHA must both be set.")

    tag_ref = f"refs/tags/{tag_name}"
    valid_ref = subprocess.run(
        ["git", "check-ref-format", tag_ref], capture_output=True, text=True
    )
    if valid_ref.returncode:
        raise SystemExit(f"Invalid release tag: {tag_name!r}")

    # Query origin directly: checkout may be shallow and omit existing tags.
    # The peeled ref resolves annotated tags to the commit they identify.
    peeled_ref = f"{tag_ref}^{{}}"
    result = subprocess.run(
        ["git", "ls-remote", "--exit-code", "origin", tag_ref, peeled_ref],
        capture_output=True,
        text=True,
    )
    if result.returncode == 2 and not result.stdout.strip():
        print(f"[release] {tag_name} does not exist yet; publishing {expected_sha}.")
        return
    if result.returncode:
        raise SystemExit(
            f"Could not check release tag {tag_name} on origin; refusing to publish. "
            f"{result.stderr.strip()}"
        )

    refs = {}
    for line in result.stdout.splitlines():
        fields = line.split()
        if len(fields) == 2 and fields[1] in (tag_ref, peeled_ref):
            refs[fields[1]] = fields[0]
    if tag_ref not in refs:
        raise SystemExit(f"Origin did not return a valid result for {tag_ref}; refusing to publish.")

    tagged_sha = refs.get(peeled_ref, refs[tag_ref])
    if tagged_sha != expected_sha:
        raise SystemExit(
            f"Refusing to publish {tag_name}: the existing tag points to {tagged_sha}, "
            f"but this run builds {expected_sha}. Bump the version in "
            "adapters/anthropic/.claude-plugin/plugin.json, commit it, and publish "
            "the matching new v<version> tag. To rebuild this release, run the "
            "workflow from its existing tag."
        )
    print(f"[release] {tag_name} matches the build commit {expected_sha}.")


if __name__ == "__main__":
    verify_release_tag(os.environ.get("RELEASE_TAG", ""), os.environ.get("RELEASE_SHA", ""))
