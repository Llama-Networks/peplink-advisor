#!/usr/bin/env python3
"""
peplink query helper.

The Peplink dataset is ~1 MB and has 103 devices with deeply nested spec sections.
Loading the whole thing into Claude's context every turn is wasteful and makes
it easy to miscite numbers. This helper projects small, targeted slices so the
model can reason over just the rows it needs.

Data file is resolved relative to this script: ../data/peplink_all_devices.json

Subcommands
-----------
  list                List every device (one line per device, name + type + series).
  show NAME           Dump the full JSON record for a single device (fuzzy match on name).
  fields              List every spec field that appears in the dataset, grouped by section.
  filter              Filter devices by type and/or a substring match on a spec field value.
  compare NAME [NAME...]   Side-by-side specs for 2+ devices, optionally narrowed to sections.
  search QUERY        Free-text substring search across names, metadata, and spec values.

All subcommands print JSON to stdout. Pipe through `jq` for pretty printing.

Examples
--------
  python query.py list --type router
  python query.py show "BR1 Pro 5G"
  python query.py filter --type router --field "5G support" --value Yes
  python query.py compare "HD2 MBX" "HD4 MBX" --sections Performance,Interfaces
  python query.py search "GPS"
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Iterable

HERE = Path(__file__).resolve().parent


def resolve_data_path() -> Path:
    """Find the dataset in both repo and packaged-adapter layouts."""
    candidates: list[Path] = []

    override = os.environ.get("PEPLINK_DATA_PATH")
    if override:
        candidates.append(Path(override).expanduser())

    candidates.extend([
        HERE.parent / "data" / "peplink_all_devices.json",  # core/scripts/query.py
        HERE / "peplink_all_devices.json",                  # ChatGPT knowledge bundle
        Path.cwd() / "peplink_all_devices.json",            # ad-hoc local runs
        Path("/mnt/data/peplink_all_devices.json"),         # Custom GPT sandbox
    ])

    for candidate in candidates:
        if candidate.exists():
            return candidate

    tried = "\n".join(f"- {candidate}" for candidate in candidates)
    raise FileNotFoundError(
        "Could not find peplink_all_devices.json. Tried:\n"
        f"{tried}\n"
        "Set PEPLINK_DATA_PATH to override the lookup path."
    )


# ---------- data loading ----------

def load() -> dict[str, Any]:
    with resolve_data_path().open("r", encoding="utf-8") as f:
        return json.load(f)


# ---------- spec walking ----------

def iter_spec_items(device: dict[str, Any]) -> Iterable[tuple[str, str, dict[str, Any]]]:
    """Yield (section, field_name, field_dict) for every leaf spec in a device.

    Handles both the deep router layout ({section: {field: {value, note}}}) and
    the flat AP/switch layout ({Specifications: {field: {value, note}}}).
    """
    specs = device.get("specifications") or {}
    for section, fields in specs.items():
        if not isinstance(fields, dict):
            continue
        for field_name, field_val in fields.items():
            if isinstance(field_val, dict):
                yield section, field_name, field_val
            else:
                # tolerate unexpected flattening
                yield section, field_name, {"value": field_val}


def find_device(data: dict[str, Any], name: str) -> dict[str, Any] | None:
    """Match a device by name. Exact (case-insensitive) first, then fuzzy."""
    name_lower = name.strip().lower()
    devices = data["devices"]

    # exact
    for d in devices:
        if d["product_name"].lower() == name_lower:
            return d

    # substring
    subs = [d for d in devices if name_lower in d["product_name"].lower()]
    if len(subs) == 1:
        return subs[0]

    # fuzzy
    names = [d["product_name"] for d in devices]
    matches = difflib.get_close_matches(name, names, n=1, cutoff=0.6)
    if matches:
        for d in devices:
            if d["product_name"] == matches[0]:
                return d

    return None


# ---------- subcommands ----------

def cmd_list(args: argparse.Namespace) -> None:
    data = load()
    out = []
    for d in data["devices"]:
        if args.type and d.get("type") != args.type:
            continue
        out.append({
            "name": d["product_name"],
            "type": d.get("type"),
            "series": d.get("metadata", {}).get("Marketing Series")
                      or d.get("metadata", {}).get("Marketing Category"),
            "product_url": d.get("metadata", {}).get("Product URL"),
        })
    print(json.dumps(out, indent=2))


def cmd_show(args: argparse.Namespace) -> None:
    data = load()
    d = find_device(data, args.name)
    if not d:
        print(json.dumps({"error": f"no device matched {args.name!r}"}, indent=2))
        sys.exit(1)
    print(json.dumps(d, indent=2))


def cmd_fields(args: argparse.Namespace) -> None:
    data = load()
    fields_by_section: dict[str, set[str]] = {}
    for d in data["devices"]:
        for section, field_name, _ in iter_spec_items(d):
            fields_by_section.setdefault(section, set()).add(field_name)
    out = {section: sorted(names) for section, names in sorted(fields_by_section.items())}
    print(json.dumps(out, indent=2))


def _value_matches(cell: dict[str, Any], needle: str | None) -> bool:
    if needle is None:
        return True
    v = str(cell.get("value", ""))
    return needle.lower() in v.lower()


def cmd_filter(args: argparse.Namespace) -> None:
    data = load()
    out = []
    field_pat = re.compile(args.field, re.IGNORECASE) if args.field else None
    for d in data["devices"]:
        if args.type and d.get("type") != args.type:
            continue
        hits = []
        for section, field_name, cell in iter_spec_items(d):
            if field_pat and not field_pat.search(field_name):
                continue
            if not _value_matches(cell, args.value):
                continue
            hits.append({
                "section": section,
                "field": field_name,
                "value": cell.get("value"),
                "note": cell.get("note"),
            })
        if (field_pat or args.value) and not hits:
            continue
        out.append({
            "name": d["product_name"],
            "type": d.get("type"),
            "matches": hits,
        })
    print(json.dumps(out, indent=2))


def cmd_compare(args: argparse.Namespace) -> None:
    data = load()
    devices = []
    for n in args.names:
        d = find_device(data, n)
        if not d:
            print(json.dumps({"error": f"no device matched {n!r}"}, indent=2))
            sys.exit(1)
        devices.append(d)

    sections_filter = None
    if args.sections:
        sections_filter = {s.strip() for s in args.sections.split(",") if s.strip()}

    # Gather every (section, field) pair any of the devices has.
    keys: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for d in devices:
        for section, field_name, _ in iter_spec_items(d):
            if sections_filter and section not in sections_filter:
                continue
            k = (section, field_name)
            if k not in seen:
                seen.add(k)
                keys.append(k)

    # Build a lookup: device -> (section, field) -> cell
    lookup: list[dict[tuple[str, str], dict[str, Any]]] = []
    for d in devices:
        m: dict[tuple[str, str], dict[str, Any]] = {}
        for section, field_name, cell in iter_spec_items(d):
            m[(section, field_name)] = cell
        lookup.append(m)

    rows = []
    for section, field_name in keys:
        row = {"section": section, "field": field_name, "values": {}}
        for d, m in zip(devices, lookup):
            cell = m.get((section, field_name))
            row["values"][d["product_name"]] = cell.get("value") if cell else None
        rows.append(row)

    print(json.dumps({
        "devices": [d["product_name"] for d in devices],
        "rows": rows,
    }, indent=2))


def cmd_search(args: argparse.Namespace) -> None:
    data = load()
    needle = args.query.lower()
    out = []
    for d in data["devices"]:
        blobs: list[tuple[str, str]] = [("name", d["product_name"])]
        for k, v in (d.get("metadata") or {}).items():
            blobs.append((f"metadata.{k}", str(v)))
        for section, field_name, cell in iter_spec_items(d):
            # Include the field name itself so queries like "GPS" match devices
            # that have a `GPS` spec field (whose value is just "Yes"/"No").
            combined = f"{section} {field_name} {cell.get('value', '')}"
            blobs.append((f"{section}.{field_name}", combined))
            if cell.get("note"):
                blobs.append((f"{section}.{field_name}.note", str(cell["note"])))
        hits = [{"where": w, "text": t} for w, t in blobs if needle in t.lower()]
        if hits:
            out.append({"name": d["product_name"], "type": d.get("type"), "hits": hits[:12]})
    print(json.dumps(out, indent=2))


# ---------- entry point ----------

def main() -> None:
    p = argparse.ArgumentParser(description="Peplink dataset query helper.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("list", help="List every device.")
    sp.add_argument("--type", choices=["router", "access_point", "switch"], default=None)
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("show", help="Show full spec for one device.")
    sp.add_argument("name")
    sp.set_defaults(func=cmd_show)

    sp = sub.add_parser("fields", help="List every spec field, grouped by section.")
    sp.set_defaults(func=cmd_fields)

    sp = sub.add_parser("filter", help="Filter by type and/or field/value.")
    sp.add_argument("--type", choices=["router", "access_point", "switch"], default=None)
    sp.add_argument("--field", help="Regex matched against field names.", default=None)
    sp.add_argument("--value", help="Substring matched against field values.", default=None)
    sp.set_defaults(func=cmd_filter)

    sp = sub.add_parser("compare", help="Compare two or more devices side by side.")
    sp.add_argument("names", nargs="+")
    sp.add_argument("--sections", help="Comma-separated section names to include.", default=None)
    sp.set_defaults(func=cmd_compare)

    sp = sub.add_parser("search", help="Free-text substring search.")
    sp.add_argument("query")
    sp.set_defaults(func=cmd_search)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
