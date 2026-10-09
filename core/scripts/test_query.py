#!/usr/bin/env python3
"""Behavioral regressions for legacy lookups and new-solution shortlists."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


QUERY = Path(__file__).with_name("query.py")


def device(name, sku, *, lifecycle=None, metadata=None):
    record = {
        "product_name": name,
        "type": "router",
        "metadata": metadata or {},
        "specifications": {"Features": {"5G support": {"value": "Yes", "note": "Requires the correct radio variant."}}},
        "sku_variants": [{"sku": sku, "addons": {"licenses": ["LIC-KEEP"], "modules": []}}],
    }
    if lifecycle:
        record["lifecycle"] = lifecycle
    return record


class LifecycleQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="peplink-query-test-")
        cls.path = Path(cls.temp.name) / "catalog.json"
        cls.legacy = {
            "status": "legacy", "source_url": "https://www.peplink.com/legacy-products/",
            "checked_on": "2026-10-09", "replacement_products": ["Balance 310 5G (HW3)"],
        }
        cls.mixed = device("BR1 Pro 5G", "MAX-BR1-PRO-5GN-T", lifecycle={
            "status": "mixed", "legacy_variants": ["5GH"], "note": "Check the exact radio SKU.",
        })
        cls.mixed["sku_variants"][0]["addons"]["modules"] = ["OLD-ADDON", "NEW-ADDON", "SHARED-SKU"]
        cls.mixed["sku_variants"].append({
            "sku": "MAX-BR1-PRO-5GH-T", "addons": {"licenses": ["LIC-KEEP"]},
            "lifecycle": cls.legacy,
        })
        cls.devices = [
            device("Balance 310 5G", "BPL-310-OLD", lifecycle=cls.legacy),
            device("Balance 310 5G (HW3)", "BPL-310-NEW", metadata={"Status": "Active"}),
            cls.mixed,
            device("Old add-on", "OLD-ADDON", lifecycle=cls.legacy),
            device("New add-on", "NEW-ADDON"),
            device("Shared old revision", "SHARED-SKU", lifecycle=cls.legacy),
            device("Shared new revision", "SHARED-SKU"),
            device("Ambiguous module", "UNCERTAIN-MODULE", lifecycle={"status": "review_required", "note": "Hardware scope unresolved."}),
            device("BR1 Mini (HW1)", "MINI-OLD", metadata={"Marketing Series": "Mobility Legacy"}),
            device("BR1 Mini", "MINI-NEW"),
        ]
        cls.metadata_blocked = []
        for number, metadata in enumerate([
            {"Status": "Component EOL"}, {"Status": "EOL"}, {"Status": "EOS"},
            {"Status": "End-of-Sale"}, {"Status": "end of life"}, {"Component Status": "EOL"},
            {"Marketing Category": "Enterprise Legacy"},
            {"Product URL": "https://www.peplink.com/legacy-products/#s04"},
        ]):
            name = f"Metadata legacy {number}"
            cls.metadata_blocked.append(name)
            cls.devices.append(device(name, f"META-{number}", metadata=metadata))
        cls.original = json.dumps({"devices": cls.devices}, indent=2)
        cls.path.write_text(cls.original)
        cls.env = {**os.environ, "PEPLINK_DATA_PATH": str(cls.path)}

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def query(self, *args, code=0):
        result = subprocess.run(
            [sys.executable, str(QUERY), *args], env=self.env,
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, code, result.stderr or result.stdout)
        return json.loads(result.stdout)

    def test_recommendation_discovery_preserves_current_revisions(self):
        for command in (("list",), ("filter", "--field", "5G support", "--value", "Yes"), ("search", "5G support")):
            with self.subTest(command=command):
                results = self.query(*command, "--new-solutions")
                names = {row["name"] for row in results}
                self.assertNotIn("Balance 310 5G", names)
                self.assertIn("Balance 310 5G (HW3)", names)
                self.assertNotIn("BR1 Mini (HW1)", names)
                self.assertIn("BR1 Mini", names)
                self.assertNotIn("Ambiguous module", names)
                self.assertTrue(all(row["lifecycle"]["new_solution_eligible"] for row in results))
                self.assertTrue(names.isdisjoint(self.metadata_blocked))

    def test_no_legacy_listing_is_not_an_active_status_claim(self):
        payload = self.query("show", "Balance 310 5G (HW3)")
        self.assertEqual(payload["lifecycle"]["status"], "not_identified_as_legacy")
        self.assertEqual(payload["lifecycle"]["vendor_status"], "Active")

    def test_mixed_parent_exposes_scope_and_filters_variants(self):
        payload = self.query("skus", "BR1 Pro 5G", "--new-solutions")
        self.assertEqual(payload["lifecycle"]["status"], "mixed")
        self.assertTrue(payload["lifecycle"]["requires_exact_sku"])
        self.assertEqual(payload["lifecycle"]["excluded_skus"], ["MAX-BR1-PRO-5GH-T"])
        self.assertEqual(payload["lifecycle"]["legacy_variants"], ["5GH"])
        self.assertEqual([v["sku"] for v in payload["sku_variants"]], ["MAX-BR1-PRO-5GN-T"])
        self.assertEqual(payload["sku_variants"][0]["addons"]["modules"], ["NEW-ADDON", "SHARED-SKU"])
        self.assertTrue(payload["sku_variants"][0]["lifecycle"]["new_solution_eligible"])

    def test_exact_legacy_sku_cannot_fuzzy_fall_back_to_current_parent(self):
        for sku in ("MAX-BR1-PRO-5GH-T", "max-br1-pro-5gh-t", "BPL-310-OLD"):
            with self.subTest(sku=sku):
                payload = self.query("skus", sku, "--new-solutions", code=1)
                self.assertIn("error", payload)
                self.assertNotIn("sku_variants", payload)
        self.query("skus", "Balance 310 5G", "--new-solutions", code=1)

    def test_sku_lists_and_search_omit_excluded_variants_and_addons(self):
        for command in (("list", "--with-skus"), ("skus",)):
            results = self.query(*command, "--new-solutions")
            row = next(r for r in results if r["name"] == "BR1 Pro 5G")
            self.assertEqual(row["skus"], ["MAX-BR1-PRO-5GN-T"])
            self.assertEqual(row["sku_count"], 1)
        self.assertEqual(self.query("search", "MAX-BR1-PRO-5GH-T", "--new-solutions"), [])
        self.assertEqual(self.query("search", "OLD-ADDON", "--new-solutions"), [])
        self.query("skus", "--find", "OLD-ADDON", "--new-solutions", code=1)
        found = self.query("skus", "--find", "LIC-KEEP", "--new-solutions")
        for row in found["matches"]:
            for match in row["matches"]:
                self.assertNotEqual(match["sku"], "MAX-BR1-PRO-5GH-T")
                self.assertTrue(match["lifecycle"]["new_solution_eligible"])

    def test_legacy_specs_skus_and_addons_remain_available(self):
        payload = self.query("show", "Balance 310 5G")
        self.assertEqual(payload["specifications"], self.devices[0]["specifications"])
        self.assertEqual(payload["sku_variants"][0]["addons"], self.devices[0]["sku_variants"][0]["addons"])
        self.assertEqual(payload["lifecycle"]["source_url"], self.legacy["source_url"])
        self.assertFalse(payload["lifecycle"]["new_solution_eligible"])
        sku = self.query("show", "MAX-BR1-PRO-5GH-T")
        self.assertFalse(sku["matched_sku"]["lifecycle"]["new_solution_eligible"])
        lookup = self.query("skus", "max-br1-pro-5gh-t")
        self.assertEqual(lookup["matches"][0]["matches"][0]["lifecycle"]["status"], "legacy")
        comparison = self.query("compare", "Balance 310 5G", "Balance 310 5G (HW3)")
        self.assertEqual(comparison["rows"][0]["values"]["Balance 310 5G"], "Yes")
        self.assertFalse(comparison["lifecycle"]["Balance 310 5G"]["new_solution_eligible"])
        mixed_comparison = self.query("compare", "MAX-BR1-PRO-5GH-T", "Balance 310 5G (HW3)")
        self.assertFalse(mixed_comparison["matched_skus"]["MAX-BR1-PRO-5GH-T"]["lifecycle"]["new_solution_eligible"])
        self.assertEqual(self.path.read_text(), self.original)

    def test_shared_sku_allows_current_revision_and_reports_ambiguity(self):
        result = self.query("skus", "shared-sku", "--new-solutions")
        matched_owners = {row["name"] for row in result["matches"] if any(hit.get("matched_sku") for hit in row["matches"])}
        self.assertEqual(matched_owners, {"Shared new revision"})
        reference = self.query("skus", "shared-sku")
        self.assertIn("Shared old revision", {row["name"] for row in reference["matches"]})
        for command in (("show", "SHARED-SKU"), ("compare", "SHARED-SKU", "BR1 Mini")):
            payload = self.query(*command, code=1)
            self.assertEqual({d["name"] for d in payload["candidates"]}, {"Shared old revision", "Shared new revision"})

    def test_unresolved_lifecycle_stays_distinct_from_legacy(self):
        payload = self.query("show", "Ambiguous module")
        self.assertEqual(payload["lifecycle"]["status"], "review_required")
        self.assertFalse(payload["lifecycle"]["new_solution_eligible"])
        self.assertEqual(payload["sku_variants"][0]["lifecycle"]["status"], "review_required")
        self.query("skus", "UNCERTAIN-MODULE", "--new-solutions", code=1)

    def test_lifecycle_appears_in_unfiltered_discovery_and_sku_results(self):
        for command in (("list",), ("filter", "--value", "Yes"), ("search", "5G support"), ("skus",)):
            with self.subTest(command=command):
                rows = self.query(*command)
                self.assertTrue(rows)
                self.assertTrue(all("new_solution_eligible" in r["lifecycle"] for r in rows))


if __name__ == "__main__":
    unittest.main()
