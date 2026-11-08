"""Offline learner examples for the patty shop, ferry and observations."""
from __future__ import annotations

import csv
import math
import re
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal as D
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"


def read_csv(name):
    with (DATA / name).open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def site_scores(weights, rows=None):
    if len(weights) != 3 or any(w < 0 for w in weights) or sum(weights) != 1:
        raise ValueError("Three nonnegative weights must sum to one.")

    def clip(score):
        return max(D(0), min(D(100), score))

    scores = {}
    for row in read_csv("patty-sites.csv") if rows is None else rows:
        count = clip(D(row["lunch_count"]))
        rent = clip(100 - (D(row["rent_jmd_month"]) - 80000) / 2000)
        access = clip(100 - 10 * D(row["hub_distance_km"]))
        scores[row["site_id"]] = sum(w * s for w, s in zip(weights, (count, rent, access)))
    return dict(sorted(scores.items(), key=lambda item: (-item[1], item[0])))


@dataclass(frozen=True)
class Lookup:
    state: str
    notice_ids: tuple[str, ...] = ()
    departure: str | None = None


def ferry_lookup(origin, destination, service_day, as_of, field="departure", rows=None):
    """All timestamps are exercise-local (Antigua and Barbuda, UTC−04:00).

    The fictional correction applies immediately when issued. Only verified
    dispatch records qualify. A response is for the exercise, not a schedule.
    """
    if not all((origin, destination, service_day, as_of)):
        return Lookup("clarify")
    if field != "departure":
        return Lookup("insufficient_evidence")
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", service_day):
        raise ValueError("Supply a service day as YYYY-MM-DD.")
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}", as_of):
        raise ValueError("Supply an as-of time as YYYY-MM-DDTHH:MM in the lab's local clock.")
    service_day = date.fromisoformat(service_day)
    as_of = datetime.fromisoformat(as_of)
    candidates = read_csv("ferry-notices.csv") if rows is None else rows
    eligible = [
        row for row in candidates
        if row["origin"] == origin and row["destination"] == destination
        and date.fromisoformat(row["service_date"]) == service_day
        and row["authority"] == "dispatch"
        and datetime.fromisoformat(row["issued_local"]) <= as_of
    ]
    by_id = {row["notice_id"]: row for row in eligible}
    replaced = set()
    for row in eligible:
        prior = by_id.get(row["supersedes"])
        if prior is None:
            continue
        if row["issued_local"] <= prior["issued_local"]:
            raise ValueError("A correction must point to an earlier eligible notice.")
        replaced.add(prior["notice_id"])
    current = sorted(
        (row for row in eligible if row["notice_id"] not in replaced),
        key=lambda row: row["notice_id"],
    )
    if not current:
        return Lookup("insufficient_evidence")
    ids = tuple(row["notice_id"] for row in current)
    times = {row["departure_local"] for row in current}
    if len(times) != 1:
        return Lookup("conflict", ids)
    return Lookup("answer", ids, times.pop())


def regional_examples():
    rows = {row["record_id"]: D(row["value"]) for row in read_csv("regional-observations.csv")}
    cto_sum = sum(rows[f"T{i:02}"] for i in range(1, 7))
    ratio = 100 * cto_sum / rows["T07"]
    all_items = 100 * (rows["J02"] - rows["J01"]) / rows["J01"]
    food_and_beverages = 100 * (rows["J04"] - rows["J03"]) / rows["J03"]
    return cto_sum, ratio, rows["T08"], all_items, rows["J05"], food_and_beverages, rows["J06"]


def main():
    priorities = tuple(map(D, ("0.55", "0.25", "0.20")))
    affordability = tuple(map(D, ("0.40", "0.45", "0.15")))
    assert site_scores(priorities) == {"K2": D("73"), "K3": D("70.25"), "K1": D("68.60")}
    assert site_scores(affordability) == {"K3": D("75.50"), "K2": D("69.50"), "K1": D("52.40")}
    assert math.isclose(math.exp(-sum(map(math.log, (1/2, 1/4, 1/8))) / 3), 4)
    test_cases = (
        (("Antigua", "Barbuda", "2031-05-18", "2031-05-18T06:30"), Lookup("answer", ("N02",), "07:30")),
        (("Antigua", "Barbuda", "2031-05-18", "2031-05-18T06:45"), Lookup("answer", ("N03",), "09:00")),
        (("Antigua", "Barbuda", "2031-05-18", "2031-05-18T07:15"), Lookup("answer", ("N03",), "09:00")),
        (("Barbuda", "Antigua", "2031-05-18", "2031-05-18T07:15"), Lookup("answer", ("N01",), "08:00")),
        ((None, "Barbuda", "2031-05-18", "2031-05-18T07:15"), Lookup("clarify")),
        (("Antigua", "Barbuda", None, "2031-05-18T07:15"), Lookup("clarify")),
        (("Antigua", "Barbuda", "2031-05-20", "2031-05-19T13:59"), Lookup("insufficient_evidence")),
        (("Antigua", "Barbuda", "2031-05-20", "2031-05-19T14:00"), Lookup("conflict", ("N06", "N07"))),
        (("Antigua", "Barbuda", "2031-05-18", "2031-05-18T07:15", "fare"), Lookup("insufficient_evidence")),
    )
    for inputs, expected in test_cases:
        assert ferry_lookup(*inputs) == expected, inputs

    invalid_times = (
        ("2031-05-18", "2031-05-18"),
        ("20310518", "2031-05-18T07:15"),
        ("2031-05-18", "2031-05-18x07:15"),
    )
    for day, as_of in invalid_times:
        try:
            ferry_lookup("Antigua", "Barbuda", day, as_of)
        except ValueError:
            continue
        raise AssertionError(f"Invalid time format accepted: {day}, {as_of}")

    # Deliberately corrupt a copy. The same comparison must reject the answer.
    corrupted = read_csv("ferry-notices.csv")
    correction = next(row for row in corrupted if row["notice_id"] == "N03")
    correction["departure_local"] = "08:59"
    inputs, expected = test_cases[2]
    assert ferry_lookup(*inputs, rows=corrupted) != expected

    cycle = read_csv("ferry-notices.csv")
    next(row for row in cycle if row["notice_id"] == "N02")["supersedes"] = "N03"
    try:
        ferry_lookup(*inputs, rows=cycle)
    except ValueError:
        pass
    else:
        raise AssertionError("A cyclic correction was accepted.")

    total, share, published, cpi, published_cpi, food, published_food = regional_examples()
    assert total == D("17.9") and share.quantize(D(".1")) == D("52.3") and published == 56
    assert cpi.quantize(D(".0001")) == D(".7725") and published_cpi == D(".8")
    assert food.quantize(D(".0001")) == D(".9548") and published_food == D(".9")
    print("Patty shop scores under first priorities", site_scores(priorities))
    print("Patty shop scores with more weight on rent", site_scores(affordability))
    print(f"Ferry lookup: {len(test_cases)} expected outcomes and five negative controls")
    print(f"CTO displayed values: {total} million, {share:.1f}%; release describes ~{published}%")
    print(f"STATIN rates: all items {cpi:.4f}% calculated and {published_cpi}% reported")
    print(f"STATIN food and non-alcoholic beverages: {food:.4f}% calculated and {published_food}% reported")


if __name__ == "__main__":
    main()
