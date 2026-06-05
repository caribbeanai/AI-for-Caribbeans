"""
Additional Caribbean datasets to support expanded course scenarios.

This generator is additive: it does not touch the files produced by
generate_datasets.py. Run after that script.

  python scripts/generate_datasets.py
  python scripts/generate_extra_datasets.py

Author: Adrian Dunkley
"""

from pathlib import Path
import csv
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "datasets"


def write_csv(name, rows, header):
    p = OUT / name
    with open(p, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {p} ({len(rows)} rows)")


def hotel_bookings_caribbean():
    rng = np.random.default_rng(101)
    destinations = ["Montego Bay", "Negril", "Bridgetown", "Castries", "Nassau",
                    "Punta Cana", "San Juan", "Aruba", "Providenciales", "Grand Cayman"]
    channels = ["booking", "expedia", "direct", "agent"]
    rows = []
    for _ in range(5000):
        dest = rng.choice(destinations)
        lead = int(rng.gamma(2.0, 30))
        nights = int(np.clip(rng.normal(5, 2), 1, 21))
        guests = int(np.clip(rng.normal(2.3, 1.0), 1, 6))
        channel = rng.choice(channels, p=[0.42, 0.18, 0.28, 0.12])
        base = {"Bridgetown": 280, "Negril": 200, "Montego Bay": 220, "Castries": 260,
                "Nassau": 300, "Punta Cana": 180, "San Juan": 240, "Aruba": 320,
                "Providenciales": 360, "Grand Cayman": 380}[dest]
        rate = max(80, base + rng.normal(0, 40))
        cancel_logit = (
            -2.0
            + (lead > 90) * 1.0
            + (channel == "booking") * 0.7
            + (channel == "expedia") * 0.5
            + (channel == "direct") * -0.6
            + (rate > base * 1.2) * 0.4
            + (guests == 1) * 0.3
        )
        prob = 1 / (1 + np.exp(-cancel_logit))
        cancelled = int(rng.random() < prob)
        rows.append([dest, lead, nights, guests, channel, round(rate, 2), cancelled])
    write_csv("hotel_bookings_caribbean.csv", rows,
              ["destination", "lead_time_days", "nights", "guests", "channel", "rate_usd", "is_cancelled"])


def cricket_matches_wi():
    rng = np.random.default_rng(11)
    opponents = ["England", "Australia", "India", "Pakistan", "South Africa",
                 "New Zealand", "Sri Lanka", "Bangladesh", "Zimbabwe", "Afghanistan"]
    venues = ["Kensington Oval", "Sabina Park", "Queen's Park Oval", "Kingsmead",
              "Brian Lara Stadium", "Daren Sammy Stadium", "Warner Park"]
    formats = ["Test", "ODI", "T20I"]
    rows = []
    for year in range(2018, 2026):
        for _ in range(28):
            fmt = rng.choice(formats, p=[0.25, 0.4, 0.35])
            opp = rng.choice(opponents)
            ven = rng.choice(venues)
            if fmt == "Test":
                wi_runs = int(rng.normal(330, 80))
                opp_runs = int(rng.normal(340, 90))
                wi_wk = int(rng.integers(5, 11))
                opp_wk = int(rng.integers(5, 11))
            elif fmt == "ODI":
                wi_runs = int(rng.normal(255, 50))
                opp_runs = int(rng.normal(260, 55))
                wi_wk = int(rng.integers(2, 11))
                opp_wk = int(rng.integers(2, 11))
            else:
                wi_runs = int(rng.normal(160, 30))
                opp_runs = int(rng.normal(165, 30))
                wi_wk = int(rng.integers(2, 11))
                opp_wk = int(rng.integers(2, 11))
            if wi_runs > opp_runs:
                result = "WI win"
            elif opp_runs > wi_runs:
                result = "WI loss"
            else:
                result = "Draw" if fmt == "Test" else "Tie"
            date = f"{year}-{int(rng.integers(1, 13)):02d}-{int(rng.integers(1, 29)):02d}"
            rows.append([date, fmt, opp, ven, wi_runs, opp_runs, wi_wk, opp_wk, result])
    write_csv("cricket_matches_wi.csv", rows,
              ["date", "format", "opponent", "venue", "wi_runs", "opp_runs",
               "wi_wickets", "opp_wickets", "result"])


def remitter_diaspora_panel():
    rng = np.random.default_rng(31)
    sources = ["USA", "Canada", "UK"]
    destinations = ["Jamaica", "Haiti", "Dominican Republic", "Guyana", "Trinidad and Tobago",
                    "Barbados", "Saint Lucia", "Saint Vincent", "Grenada", "Antigua and Barbuda"]
    rows = []
    base = {"Jamaica": 220, "Haiti": 350, "Dominican Republic": 700, "Guyana": 80,
            "Trinidad and Tobago": 110, "Barbados": 40, "Saint Lucia": 35, "Saint Vincent": 30,
            "Grenada": 32, "Antigua and Barbuda": 25}
    for year in range(2018, 2026):
        for month in range(1, 13):
            for src in sources:
                src_mult = {"USA": 1.0, "Canada": 0.18, "UK": 0.22}[src]
                seasonal = 1 + 0.18 * (month in (11, 12, 8))
                covid = 0.7 if (year == 2020 and 4 <= month <= 9) else 1.0
                for dst in destinations:
                    vol = base[dst] * src_mult * seasonal * covid * (1 + (year - 2018) * 0.03)
                    vol = max(0, vol + rng.normal(0, vol * 0.05))
                    rows.append([year, month, src, dst, round(vol, 2)])
    write_csv("remitter_diaspora_panel.csv", rows,
              ["year", "month", "from_country", "to_country", "volume_usd_millions"])


def fishing_landings():
    rng = np.random.default_rng(41)
    ports = ["Castries", "Soufriere", "Kingstown", "Saint George's", "Roseau", "Saint John's"]
    species = ["snapper", "lobster", "kingfish", "mahi mahi", "lionfish", "tuna"]
    rows = []
    for day in range(540):
        year = 2024 + day // 365
        date = f"{year}-{((day // 30) % 12) + 1:02d}-{(day % 28) + 1:02d}"
        for port in ports:
            for sp in species:
                base_weight = {"snapper": 90, "lobster": 30, "kingfish": 60,
                               "mahi mahi": 75, "lionfish": 12, "tuna": 110}[sp]
                seasonal = 1 + 0.3 * (sp == "lobster" and ((day % 365) > 90 and (day % 365) < 240))
                w = max(0, base_weight * seasonal + rng.normal(0, base_weight * 0.2))
                p = {"snapper": 9, "lobster": 30, "kingfish": 11,
                     "mahi mahi": 12, "lionfish": 6, "tuna": 14}[sp] + rng.normal(0, 1)
                rows.append([date, port, sp, round(w, 1), round(max(p, 3), 2)])
    write_csv("fishing_landings.csv", rows, ["date", "port", "species", "weight_kg", "price_per_kg_usd"])


def solar_irradiance():
    rng = np.random.default_rng(53)
    sites = ["Kingston", "Bridgetown", "Castries"]
    rows = []
    for day in range(365):
        for hour in range(6, 19):
            t = day * 24 + hour
            for site in sites:
                base = max(0, 900 * np.sin(np.pi * (hour - 6) / 12))
                cloud = float(np.clip(rng.normal(35, 15), 5, 90))
                ghi = base * (1 - cloud / 200) + rng.normal(0, 25)
                temp = 26 + 4 * np.sin(np.pi * (hour - 6) / 12) + rng.normal(0, 0.7)
                timestamp = f"2025-{((day // 30) % 12) + 1:02d}-{(day % 28) + 1:02d}T{hour:02d}:00"
                rows.append([timestamp, site, round(max(ghi, 0), 1), round(temp, 2), round(cloud, 1)])
    write_csv("solar_irradiance.csv", rows, ["timestamp", "site", "ghi_w_m2", "temperature_c", "cloud_cover_pct"])


def school_attendance():
    rng = np.random.default_rng(67)
    schools = [("Kingston College", "Saint Andrew"), ("Wolmer's Girls", "Kingston"),
               ("Combermere", "Saint Michael"), ("Saint Joseph's Convent", "Castries"),
               ("Queen's Royal College", "Port of Spain")]
    rows = []
    for day in range(220):
        date = f"2025-{((day // 22) % 12) + 1:02d}-{(day % 28) + 1:02d}"
        rain = max(0, rng.normal(8, 12))
        exam_term = int((day // 60) % 2 == 1)
        for name, parish in schools:
            base = 0.94 - 0.0015 * rain - 0.02 * exam_term
            att = float(np.clip(rng.normal(base, 0.04), 0.6, 1.0))
            rows.append([date, name, parish, round(att * 100, 1), round(rain, 1), exam_term])
    write_csv("school_attendance.csv", rows, ["date", "school", "parish", "attendance_pct", "rainfall_mm", "is_exam_term"])


def health_clinic_visits():
    rng = np.random.default_rng(73)
    parishes = ["Saint Andrew", "Saint Catherine", "Saint James", "Kingston", "Manchester"]
    reasons = ["dengue_suspect", "hypertension", "diabetes", "prenatal", "injury"]
    rows = []
    for day in range(540):
        year = 2024 + day // 365
        date = f"{year}-{((day // 30) % 12) + 1:02d}-{(day % 28) + 1:02d}"
        rainy_month = ((day // 30) % 12) + 1 in (8, 9, 10, 11)
        for par in parishes:
            for r in reasons:
                base = {"dengue_suspect": 6 if rainy_month else 2,
                        "hypertension": 18, "diabetes": 14,
                        "prenatal": 8, "injury": 9}[r]
                visits = max(0, int(rng.poisson(base)))
                rows.append([date, par, r, visits])
    write_csv("health_clinic_visits.csv", rows, ["date", "parish", "reason", "visits"])


def carnival_attendance():
    rng = np.random.default_rng(79)
    events = {
        "Trinidad and Tobago": ["Panorama", "Dimanche Gras", "Jouvert", "Monday Mas", "Tuesday Mas"],
        "Barbados": ["Foreday Morning", "Grand Kadooment"],
        "Saint Lucia": ["Carnival Monday", "Carnival Tuesday"],
        "Saint Vincent and the Grenadines": ["Mardi Gras", "Jouvert", "Tuesday Mas"],
        "Grenada": ["Jab Jab", "Monday Mas", "Tuesday Mas"],
    }
    rows = []
    for year in range(2018, 2026):
        if year in (2020, 2021):
            continue
        for country, days in events.items():
            base = {"Trinidad and Tobago": 100_000, "Barbados": 50_000,
                    "Saint Lucia": 25_000, "Saint Vincent and the Grenadines": 18_000, "Grenada": 22_000}[country]
            for ed in days:
                att = int(base * float(rng.uniform(0.6, 1.3)))
                rows.append([country, year, ed, att])
    write_csv("carnival_attendance.csv", rows, ["country", "year", "event_day", "attendance"])


def real_estate_listings():
    rng = np.random.default_rng(89)
    cities = [
        ("New Kingston", "Kingston", "JMD", 6_500),
        ("Liguanea", "Kingston", "JMD", 5_200),
        ("Cherry Gardens", "Kingston", "JMD", 5_800),
        ("Westmoorings", "Port of Spain", "TTD", 95),
        ("Cap Estate", "Castries", "XCD", 35),
        ("Christ Church", "Bridgetown", "BBD", 28),
        ("Bavaro", "Punta Cana", "DOP", 95_000),
        ("Cole Bay", "Sint Maarten", "USD", 4),
    ]
    rows = []
    for neigh, city, currency, price_per_sqft in cities:
        for _ in range(150):
            beds = int(rng.integers(1, 5))
            baths = max(1, beds - int(rng.integers(0, 2)))
            sqft = int(np.clip(rng.normal(900 + beds * 250, 200), 400, 4000))
            price = sqft * price_per_sqft * float(rng.uniform(0.8, 1.25))
            rows.append([city, neigh, beds, baths, sqft, round(price, 0), currency])
    write_csv("real_estate_listings.csv", rows,
              ["city", "neighbourhood", "beds", "baths", "sqft", "price_local", "currency"])


def main():
    hotel_bookings_caribbean()
    cricket_matches_wi()
    remitter_diaspora_panel()
    fishing_landings()
    solar_irradiance()
    school_attendance()
    health_clinic_visits()
    carnival_attendance()
    real_estate_listings()


if __name__ == "__main__":
    main()
