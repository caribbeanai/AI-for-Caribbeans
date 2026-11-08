"""Build and validate source-bound lookup exercises for the place index."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
PREFIX = {"core": "C", "islands": "I", "wider": "W"}


def indexed_places():
    counts = dict.fromkeys(PREFIX, 0)
    with (DATA / "places.tsv").open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file, delimiter="\t"):
            group = row["group"]
            counts[group] += 1
            row["case_id"] = f"{PREFIX[group]}{counts[group]:02}"
            yield row


def lookup(records, place_key, field, as_of):
    eligible = [
        r for r in records if r["place_key"] == place_key and r["field"] == field
        and r["approved"] and r["issued_local"] <= as_of
    ]
    return max(eligible, key=lambda r: r["issued_local"], default=None)


def build_cases():
    with (DATA / "place-case-values.tsv").open(encoding="utf-8", newline="") as file:
        values = {row["case_id"]: row for row in csv.DictReader(file, delimiter="\t")}
    cases = {}
    for row in indexed_places():
        cid = row["case_id"]
        value = values.pop(cid)
        field = value["field"]
        case = {
            "place_en": row["place_en"], "place_es": row["place_es"],
            "task_en": row["task_en"], "task_es": row["task_es"],
            "field": field, "unit": value["unit"],
            "provenance": "fictional teaching example",
            "records": [
                {"id": cid + "-A", "place_key": cid, "field": field,
                 "value": value["approved"], "approved": True, "issued_local": "2031-06-01T08:00"},
                {"id": cid + "-B", "place_key": cid, "field": field,
                 "value": value["distractor"], "approved": False, "issued_local": "2031-06-01T08:10"},
            ],
            "as_of": "2031-06-01T08:30",
            "expected_id": cid + "-A", "expected_value": value["approved"],
        }
        cases[cid] = case
    if values:
        raise ValueError(f"Unmatched cases: {sorted(values)}")
    return cases


def verify(cases):
    records = [r for c in cases.values() for r in c["records"]]
    for cid, c in cases.items():
        got = lookup(records, cid, c["field"], c["as_of"])
        assert (got["id"], got["value"]) == (c["expected_id"], c["expected_value"])
        assert lookup(records, cid, c["field"], "2031-06-01T07:59") is None
        assert lookup(records, cid, "unsupported_field", c["as_of"]) is None
        assert lookup(records, "not-in-index", c["field"], c["as_of"]) is None
        bad = [dict(r, approved=True) if r["id"] == cid + "-B" else r for r in records]
        assert lookup(bad, cid, c["field"], c["as_of"])["value"] != c["expected_value"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("case_id", nargs="?")
    parser.add_argument("--export", action="store_true")
    args = parser.parse_args()
    cases = build_cases()
    verify(cases)
    if args.export:
        (DATA / "place-lab-cases.json").write_text(
            json.dumps(cases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    if args.case_id:
        print(json.dumps(cases[args.case_id], ensure_ascii=False, indent=2))
    else:
        print(f"{len(cases)} indexed places verified with known, stale, out-of-scope and mutated controls.")


if __name__ == "__main__":
    main()
