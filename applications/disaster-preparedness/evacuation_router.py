"""
Toy evacuation router. Routes residents to the nearest shelter with capacity.

Author: Adrian Dunkley
"""

import math
from dataclasses import dataclass


@dataclass
class Place:
    name: str
    lat: float
    lon: float


@dataclass
class Shelter(Place):
    capacity: int


def haversine_km(a: Place, b: Place) -> float:
    R = 6371.0
    lat1, lat2 = math.radians(a.lat), math.radians(b.lat)
    dlat = math.radians(b.lat - a.lat)
    dlon = math.radians(b.lon - a.lon)
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def assign(residents, shelters):
    used = {s.name: 0 for s in shelters}
    plan = []
    for r in residents:
        ordered = sorted(shelters, key=lambda s: haversine_km(r, s))
        for s in ordered:
            if used[s.name] < s.capacity:
                used[s.name] += 1
                plan.append((r.name, s.name, round(haversine_km(r, s), 2)))
                break
        else:
            plan.append((r.name, "NO SHELTER", None))
    return plan


if __name__ == "__main__":
    shelters = [
        Shelter("Half Way Tree High School", 18.012, -76.794, capacity=3),
        Shelter("Mona Heights Primary", 18.005, -76.745, capacity=2),
        Shelter("Spanish Town Community Centre", 17.991, -76.953, capacity=4),
    ]
    residents = [
        Place("Family A, Liguanea", 18.010, -76.760),
        Place("Family B, Constant Spring", 18.040, -76.793),
        Place("Family C, Portmore", 17.948, -76.882),
        Place("Family D, Spanish Town", 17.991, -76.953),
        Place("Family E, August Town", 18.014, -76.744),
        Place("Family F, Stony Hill", 18.054, -76.787),
    ]
    for resident, shelter, dist in assign(residents, shelters):
        print(f"{resident:35} -> {shelter:35} {dist} km" if dist is not None else f"{resident} -> {shelter}")
