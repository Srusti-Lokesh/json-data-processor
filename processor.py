
"""Command-line JSON processor for employee, product, and student records."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent / "data"
VALID_DATASETS = {"employees", "products", "students"}

def load_records(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list) or any(not isinstance(row, dict) for row in data):
        raise ValueError("Input JSON must be an array of objects.")
    return data

def process(records: list[dict[str, Any]], query: str = "", field: str = "", value: str = "") -> list[dict[str, Any]]:
    output = []
    for row in records:
        if query and query.casefold() not in json.dumps(row, ensure_ascii=False).casefold():
            continue
        if field and value:
            if field not in row or value.casefold() not in str(row[field]).casefold():
                continue
        output.append(row)
    return output

def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {"record_count": len(records), "fields": sorted({k for r in records for k in r})}
    numeric: dict[str, dict[str, float]] = {}
    for key in summary["fields"]:
        vals = [r[key] for r in records if isinstance(r.get(key), (int, float)) and not isinstance(r.get(key), bool)]
        if vals:
            numeric[key] = {"min": min(vals), "max": max(vals), "average": round(sum(vals) / len(vals), 2)}
    summary["numeric_fields"] = numeric
    return summary

def main() -> int:
    parser = argparse.ArgumentParser(description="Search, filter, and summarize JSON records.")
    parser.add_argument("--dataset", choices=sorted(VALID_DATASETS), default="employees")
    parser.add_argument("--input", help="Optional path to a JSON array file; overrides --dataset.")
    parser.add_argument("--query", default="", help="Case-insensitive text search across each record.")
    parser.add_argument("--field", default="", help="Field name to filter when --value is supplied.")
    parser.add_argument("--value", default="", help="Case-insensitive substring for the selected field.")
    parser.add_argument("--output", help="Optional path to write matched records as JSON.")
    parser.add_argument("--summary", action="store_true", help="Print summary of matched records.")
    args = parser.parse_args()
    path = Path(args.input).expanduser() if args.input else DATA_DIR / f"{args.dataset}.json"
    try:
        records = load_records(path)
        matched = process(records, args.query, args.field, args.value)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(matched, indent=2, ensure_ascii=False))
    if args.summary:
        print("\nSummary:")
        print(json.dumps(summarize(matched), indent=2, ensure_ascii=False))
    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as handle:
            json.dump(matched, handle, indent=2, ensure_ascii=False)
        print(f"\nSaved {len(matched)} records to {output_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
