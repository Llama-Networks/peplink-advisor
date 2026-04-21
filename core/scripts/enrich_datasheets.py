#!/usr/bin/env python3
"""Add `datasheet_url` to each device's metadata by probing known Peplink URL patterns.

Peplink hosts datasheet PDFs under two conventions, and they are not totally
consistent. We try candidates in order and keep the first one that returns
HTTP 200 with a PDF content type. Devices with no verified datasheet get a
`datasheet_url` of null — fall back to `Product URL` in that case.

Usage
-----
    python3 enrich_datasheets.py           # enrich in place
    python3 enrich_datasheets.py --dry-run # print but don't write
    python3 enrich_datasheets.py --only "HD2 MBX 5G,Balance 20X"  # probe subset

Safe to re-run when the dataset refreshes.
"""
from __future__ import annotations
import argparse, json, os, re, sys, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.normpath(os.path.join(HERE, "..", "data", "peplink_all_devices.json"))

UA = "peplink-advisor-enricher/0.1 (+internal; polite probing)"
TIMEOUT = 15


def slugify(name: str, sep: str = "-") -> str:
    """Lowercase, strip punctuation, collapse whitespace to `sep`."""
    s = name.lower()
    s = s.replace("(", " ").replace(")", " ")
    s = re.sub(r"[^a-z0-9]+", sep, s)
    s = s.strip(sep)
    return s


def candidates(name: str) -> list[str]:
    kebab = slugify(name, "-")
    snake = slugify(name, "_")
    urls = [
        # pattern 1: peplink.com tech-specs (most routers + switches)
        f"https://www.peplink.com/compare/tech-specs/{kebab}.pdf",
        # pattern 2: download.peplink.com with pepwave_ prefix (APs, some mobility)
        f"https://download.peplink.com/resources/pepwave_{snake}_datasheet.pdf",
        # pattern 3: download.peplink.com with peplink_ prefix (some stationary)
        f"https://download.peplink.com/resources/peplink_{snake}_datasheet.pdf",
    ]
    # For names beginning with a family prefix (HD2/HD4/BR1/…), strip the prefix
    # and retry pepwave_ — Peplink sometimes omits the series in the filename.
    tokens = snake.split("_")
    if len(tokens) > 1:
        stripped = "_".join(tokens[1:])
        urls.append(f"https://download.peplink.com/resources/pepwave_{stripped}_datasheet.pdf")
    return urls


def probe(url: str) -> bool:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            ct = resp.headers.get("Content-Type", "").lower()
            return resp.status == 200 and ct.startswith("application/pdf")
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        return False


def find_datasheet(name: str, verbose: bool = False) -> str | None:
    for url in candidates(name):
        ok = probe(url)
        if verbose:
            print(("hit  " if ok else "miss "), url)
        if ok:
            return url
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", default=None, help="Comma-separated list of product names to probe.")
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    targets = set()
    if args.only:
        targets = {n.strip().lower() for n in args.only.split(",") if n.strip()}

    hits, misses = 0, 0
    for dev in data["devices"]:
        name = dev["product_name"]
        if targets and name.lower() not in targets:
            continue
        url = find_datasheet(name, verbose=args.verbose)
        meta = dev.setdefault("metadata", {})
        meta["Datasheet URL"] = url
        if url:
            hits += 1
            print(f"[+] {name:35s} {url}")
        else:
            misses += 1
            print(f"[ ] {name:35s} (no datasheet found)")

    print(f"\n{hits} matched, {misses} not found.")

    if args.dry_run:
        print("(dry run: dataset not modified)")
        return

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"wrote {DATA_PATH}")


if __name__ == "__main__":
    main()
