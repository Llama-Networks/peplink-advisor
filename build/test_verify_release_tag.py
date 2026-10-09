"""Exercise release protection against real lightweight and annotated Git tags."""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("verify_release_tag.py").resolve()


class ReleaseTagTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="peplink-release-test-")
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.repo = root / "work"
        self.remote = root / "origin.git"
        self.repo.mkdir()
        self.git("init", "--bare", str(self.remote))
        self.git("init")
        self.git("config", "user.name", "Release test")
        self.git("config", "user.email", "release-test@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "tag.gpgsign", "false")
        self.git("remote", "add", "origin", str(self.remote))
        self.git("commit", "--allow-empty", "-m", "Original release")
        self.old_sha = self.git("rev-parse", "HEAD")
        self.git("commit", "--allow-empty", "-m", "Updated catalog")
        self.new_sha = self.git("rev-parse", "HEAD")
        self.git("push", "origin", "HEAD:refs/heads/main")

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.repo, check=True, capture_output=True, text=True
        ).stdout.strip()

    def publish_tag(self, tag="v0.2.2", sha=None, annotated=False):
        args = ["tag"]
        if annotated:
            args += ["-a", "-m", "Release"]
        self.git(*args, tag, sha or self.old_sha)
        self.git("push", "origin", f"refs/tags/{tag}")
        # Simulate a checkout that lacks local tags; the guard must query origin.
        self.git("tag", "-d", tag)

    def verify(self, tag="v0.2.2", sha=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=self.repo,
            env={**os.environ, "RELEASE_TAG": tag, "RELEASE_SHA": sha or self.new_sha},
            capture_output=True,
            text=True,
        )

    def test_rejects_new_main_commit_for_existing_release(self):
        self.publish_tag()
        result = self.verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(self.old_sha, result.stderr)
        self.assertIn(self.new_sha, result.stderr)
        self.assertIn("Bump the version", result.stderr)

    def test_accepts_matching_lightweight_tag(self):
        self.publish_tag()
        result = self.verify(sha=self.old_sha)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_accepts_matching_annotated_tag(self):
        self.publish_tag(annotated=True)
        result = self.verify(sha=self.old_sha)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_mismatched_annotated_tag(self):
        self.publish_tag(annotated=True)
        result = self.verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(self.old_sha, result.stderr)

    def test_accepts_new_tag(self):
        result = self.verify(tag="v0.2.3")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("does not exist yet", result.stdout)

    def test_does_not_match_similarly_named_tag(self):
        self.publish_tag(tag="archive/v0.2.2")
        result = self.verify()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("does not exist yet", result.stdout)

    def test_fails_closed_when_remote_is_unavailable(self):
        self.git("remote", "set-url", "origin", str(self.remote / "missing"))
        result = self.verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Could not check release tag", result.stderr)
        self.assertIn("refusing to publish", result.stderr)

    def test_rejects_tag_patterns(self):
        result = self.verify(tag="v*")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid release tag", result.stderr)


if __name__ == "__main__":
    unittest.main()
