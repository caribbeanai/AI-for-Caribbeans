"""
Generate the synthetic Caribbean datasets used across the repo.

Synthetic is honest here: public Caribbean data is uneven, and using made up
data lets us teach without licensing fragility. The patterns reflect
plausible regional realities. Do not use these files for research claims.

Run from repo root:
  python scripts/generate_datasets.py

Author: Adrian Dunkley
"""

from pathlib import Path
import csv
import json
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


def saint_lucia_rainfall():
    rng = np.random.default_rng(7)
    rows = []
    for year in range(2010, 2026):
        for month in range(1, 13):
            seasonal = 80 + 140 * max(0, np.sin(np.pi * (month - 5) / 7))
            temp = 26 + 2 * np.sin(2 * np.pi * (month - 4) / 12) + rng.normal(0, 0.4)
            rain = max(0, seasonal + rng.normal(0, 30))
            rows.append([month, year, round(temp, 2), round(rain, 1)])
    write_csv("saint_lucia_rainfall.csv", rows, ["month", "year", "mean_temp_c", "rainfall_mm"])


def caribbean_mangoes():
    rng = np.random.default_rng(42)
    rows = []
    for variety, length_mu, width_mu, weight_mu, brix_mu in [
        ("Julie", 7.5, 6.0, 220, 17),
        ("East Indian", 13.0, 6.5, 350, 14),
        ("Bombay", 10.5, 7.2, 320, 15),
        ("Number Eleven", 8.5, 6.5, 260, 18),
    ]:
        for _ in range(60):
            rows.append([
                round(rng.normal(length_mu, 0.5), 2),
                round(rng.normal(width_mu, 0.4), 2),
                int(rng.normal(weight_mu, 25)),
                round(rng.normal(brix_mu, 1.0), 2),
                variety,
            ])
    rng.shuffle(rows)
    write_csv("caribbean_mangoes.csv", rows, ["length_cm", "width_cm", "weight_g", "sweetness_brix", "variety"])


def barbados_arrivals():
    rng = np.random.default_rng(3)
    rows = []
    base = 38000
    for year in range(2014, 2026):
        for month in range(1, 13):
            seasonal = 1 + 0.35 * np.cos(2 * np.pi * (month - 1) / 12)
            growth = 1 + (year - 2014) * 0.015
            covid = 0.2 if (year == 2020 and 4 <= month <= 12) or (year == 2021 and month <= 5) else 1.0
            value = int(base * seasonal * growth * covid + rng.normal(0, 1500))
            date = f"{year}-{month:02d}-01"
            rows.append([date, max(0, value)])
    write_csv("barbados_arrivals.csv", rows, ["date", "arrivals"])


def tourism_reviews():
    samples = [
        ("Beautiful beach and turquoise water, perfect family vacation in Negril.", "positive"),
        ("Hotel staff in Bridgetown were friendly but the rooms were dated.", "mixed"),
        ("The breakfast buffet had too few local options, more bake and shark please.", "negative"),
        ("Wonderful weekend in Soufriere, the Pitons view from our room was unreal.", "positive"),
        ("AC was broken for two nights in Castries and no one came to fix it.", "negative"),
        ("Carnival in Trinidad was a vibe, mas band well organised, fete every night.", "positive"),
        ("Pricey but the service in Saint John, USVI was top tier, would return.", "positive"),
        ("Slow check in at Lynden Pindling airport but our Nassau resort made up for it.", "mixed"),
        ("Loved the food in Roseau, Dominica is truly the nature isle.", "positive"),
        ("Beach in Punta Cana was crowded, all inclusive food was bland.", "negative"),
        ("Great snorkelling off Tobago Cays, our boat captain knew every reef.", "positive"),
        ("Front desk in Willemstad spoke four languages effortlessly, big plus.", "positive"),
        ("Rooms in Half Moon Bay had lovely views but the pool was cold.", "mixed"),
        ("Dinner at the local restaurant in San Juan was excellent, mofongo was perfect.", "positive"),
        ("Tour guide in Saint Vincent was knowledgeable and patient with kids.", "positive"),
        ("Heavy rain ruined our day in Anguilla but the hotel offered a free spa day.", "mixed"),
        ("Hotel in Holetown overpromised and underdelivered on the beachfront pitch.", "negative"),
        ("Loved Junkanoo on Bay Street, energy and costumes were stunning.", "positive"),
        ("Conch fritters in Providenciales were the best I have ever had.", "positive"),
        ("Slow service at the bar in Montego Bay, drinks took 25 minutes.", "negative"),
        ("Diving the Blue Hole in Belize was a once in a lifetime experience.", "positive"),
        ("Hotel charged us twice and took weeks to refund in Saint Lucia.", "negative"),
        ("Beach in Grand Anse was perfect for our honeymoon in Grenada.", "positive"),
        ("Front desk in Aruba was kind, hot tub did not work both nights.", "mixed"),
        ("Pico Duarte hike was tough but our guide in Santo Domingo was excellent.", "positive"),
        ("Old Havana was magical, the food was simple but the music made the trip.", "positive"),
        ("Spent too much on excursions in Antigua, half the activities cancelled.", "negative"),
        ("Loved Anegada's lobsters, BVI sailing was smooth and uncrowded.", "positive"),
        ("Concierge in Hamilton, Bermuda was professional and discreet, will return.", "positive"),
        ("Hotel WiFi in Basseterre was unusable, important emails missed.", "negative"),
        ("Rainforest hike in Saint Lucia made up for the rain.", "positive"),
        ("Bay Gardens Hotel in Castries was clean and the breakfast was hearty.", "positive"),
        ("Booked an overwater bungalow but ours was a regular room, disappointing.", "negative"),
        ("Local guide in Suriname showed us a side of Paramaribo I did not expect.", "positive"),
        ("Dinner in Holetown was delicious, the macaroni pie was perfect.", "positive"),
    ]
    rows = [[i, s, label] for i, (s, label) in enumerate(samples)]
    write_csv("tourism_reviews.csv", rows, ["id", "review", "label"])


def remittance_transactions():
    rng = np.random.default_rng(11)
    rows = []
    for i in range(3000):
        amount = float(rng.gamma(2, 200))
        sender_risk = rng.integers(0, 5)
        age_days = int(rng.exponential(800))
        hour = int(rng.integers(0, 24))
        channel = rng.choice([0, 1, 2])
        chan_atm = int(channel == 0)
        chan_branch = int(channel == 1)
        chan_online = int(channel == 2)
        score = (
            (amount > 1500) * 0.7
            + (sender_risk >= 3) * 1.2
            + (age_days < 30) * 1.5
            + (hour < 5 or hour > 22) * 0.6
            + (channel == 2 and amount > 800) * 0.5
        )
        prob = 1 / (1 + np.exp(-score + 1.5))
        suspicious = int(rng.random() < prob)
        rows.append([round(amount, 2), sender_risk, age_days, hour, chan_atm, chan_branch, chan_online, suspicious])
    write_csv(
        "remittance_transactions.csv", rows,
        ["amount_usd", "sender_country_risk", "receiver_account_age_days",
         "hour_of_day", "channel_atm", "channel_branch", "channel_online", "is_suspicious"],
    )


def yam_yield():
    rng = np.random.default_rng(13)
    parishes = ["Saint Mary", "Trelawny", "Saint Elizabeth", "Manchester", "Saint Ann", "Westmoreland"]
    rows = []
    for _ in range(600):
        parish = rng.choice(parishes)
        rainfall = float(rng.normal(1300, 250))
        fert = float(rng.normal(80, 25))
        acres = float(np.clip(rng.normal(3, 1.2), 0.5, 8))
        base = {"Saint Mary": 5000, "Trelawny": 5400, "Saint Elizabeth": 4500,
                "Manchester": 4800, "Saint Ann": 5200, "Westmoreland": 4700}[parish]
        yield_kg = base + (rainfall - 1300) * 1.6 + (fert - 80) * 18 + rng.normal(0, 300)
        rows.append([parish, round(rainfall, 1), round(fert, 1), round(acres, 2), round(yield_kg, 1)])
    write_csv("yam_yield.csv", rows, ["parish", "rainfall_mm", "fertiliser_kg_per_acre", "area_acres", "yield_kg_per_acre"])


def market_prices_weekly():
    rng = np.random.default_rng(17)
    items = {"yam": 180, "callaloo": 120, "tomato": 200, "scotch bonnet": 350,
             "sweet potato": 140, "plantain": 90}
    rows = []
    for week in range(104):
        year = 2024 + (week // 52)
        wk_of_year = (week % 52) + 1
        for item, baseline in items.items():
            seasonal = 1 + 0.15 * np.sin(2 * np.pi * wk_of_year / 52)
            shock = 1.4 if (week == 60 and item == "scotch bonnet") else 1.0
            price = baseline * seasonal * shock + rng.normal(0, 6)
            date = f"{year}-W{wk_of_year:02d}"
            rows.append([date, item, round(max(price, 30), 1)])
    write_csv("market_prices_weekly.csv", rows, ["date", "item", "price_jmd_per_lb"])


def atlantic_storms():
    rng = np.random.default_rng(23)
    rows = []
    for _ in range(400):
        init_wind = float(rng.uniform(30, 95))
        init_pres = float(rng.uniform(975, 1005))
        sst = float(rng.uniform(26.5, 30.5))
        shear = float(rng.uniform(2, 22))
        lat = float(rng.uniform(10, 22))
        lon = float(rng.uniform(-80, -50))
        peak = init_wind + (sst - 27) * 20 - shear * 2.5 + rng.normal(0, 12)
        peak = float(np.clip(peak, 40, 180))
        rows.append([round(init_wind, 1), round(init_pres, 1), round(sst, 2), round(shear, 1),
                     round(lat, 2), round(lon, 2), round(peak, 1)])
    write_csv("atlantic_storms.csv", rows,
              ["init_wind_mph", "init_pressure_mb", "sst_c", "shear_kt", "lat", "lon", "peak_wind_mph"])


def sea_level_monthly():
    rng = np.random.default_rng(29)
    rows = []
    trend_mm_per_year = 3.4
    intercept = 7000
    for year in range(1990, 2026):
        for month in range(1, 13):
            t = (year - 1990) * 12 + month
            level = intercept + trend_mm_per_year * (t / 12) + 18 * np.sin(2 * np.pi * month / 12) + rng.normal(0, 8)
            rows.append([year, month, round(level, 1)])
    write_csv("sea_level_monthly.csv", rows, ["year", "month", "level_mm"])


def sst_anomaly():
    rng = np.random.default_rng(31)
    sites = ["Cayman Reefs", "Belize Barrier", "Tobago Cays", "Bonaire Marine Park", "Saba Bank"]
    rows = []
    for year in range(2018, 2026):
        for month in range(1, 13):
            for site in sites:
                base = 0.4 + 0.6 * max(0, np.sin(2 * np.pi * (month - 7) / 12))
                spike = 1.2 if (year >= 2023 and month in (8, 9, 10)) else 0
                anomaly = base + spike + rng.normal(0, 0.3)
                rows.append([year, month, site, round(anomaly, 2)])
    write_csv("sst_anomaly.csv", rows, ["year", "month", "site", "sst_anomaly_c"])


def caribbean_dialect_phrases():
    data = [
        ("Jamaica", "Wah gwaan? Mi deh yah enuh."),
        ("Jamaica", "Likkle more, mi soon come back."),
        ("Jamaica", "Mi nah lie, di pickney dem hungry."),
        ("Trinidad and Tobago", "Allyuh ready for de fete tonight?"),
        ("Trinidad and Tobago", "I going to lime in Maracas later."),
        ("Trinidad and Tobago", "Doh dotish nah, drive careful."),
        ("Barbados", "Wuh part yuh deh? Lewwe go down by de gap."),
        ("Barbados", "Cheese on bread, this rain ent stopping."),
        ("Saint Lucia", "Sa ka fèt? Mwen byen, mèsi."),
        ("Saint Lucia", "Annou alé bò lanmè."),
        ("Dominica", "Sa ka rivé? Tout bagay anlè."),
        ("Grenada", "Whey yuh going? Down by de fish fry."),
        ("Saint Vincent and the Grenadines", "Yuh good? Tek time wid de road."),
        ("Antigua and Barbuda", "Wha gwan dey? Me gone home now."),
        ("Saint Kitts and Nevis", "Wha appenin nuh, mi deh yah."),
        ("Bahamas", "Wha goin on bey? Sip sip running heavy."),
        ("Belize", "Weh di go aan? Da how yu di du?"),
        ("Guyana", "Banna, awee going downtown lata."),
        ("Suriname", "Fa waka? Mi e go na wowoyo."),
        ("Haiti", "Sak pase? N ap boule, mèsi."),
        ("Dominican Republic", "Que lo que? Manín, todo bien."),
        ("Cuba", "Asere, que volá? Todo bien aquí."),
        ("Puerto Rico", "Wepa, brutal el concierto anoche."),
        ("Aruba", "Bon dia, con ta bay? Mi ta bon."),
        ("Curaçao", "Bon bini, kon ta bai? Hopi bon."),
        ("British Virgin Islands", "Wha goin on, bey? Just liming."),
        ("United States Virgin Islands", "Wha goin on cuz, just bambye."),
        ("Bermuda", "Innit nice today, bie? Goin tarn now."),
        ("Cayman Islands", "Wha goin on bro, jus chillin."),
        ("Turks and Caicos", "Wassup my dear, all good."),
    ]
    rows = [[c, p] for c, p in data]
    write_csv("caribbean_dialect_phrases.csv", rows, ["country", "phrase"])


def supermarket_customers():
    rng = np.random.default_rng(37)
    rows = []
    for _ in range(1200):
        segment = rng.choice(["weekly_family", "weekend_bulk", "daily_topup", "premium"], p=[0.4, 0.25, 0.25, 0.10])
        if segment == "weekly_family":
            spend, visits, fresh, ticket = rng.normal(2800, 400), rng.normal(4, 1), rng.normal(0.35, 0.07), rng.normal(720, 80)
        elif segment == "weekend_bulk":
            spend, visits, fresh, ticket = rng.normal(3200, 500), rng.normal(2, 0.7), rng.normal(0.30, 0.05), rng.normal(1500, 200)
        elif segment == "daily_topup":
            spend, visits, fresh, ticket = rng.normal(1800, 300), rng.normal(14, 3), rng.normal(0.45, 0.08), rng.normal(130, 25)
        else:
            spend, visits, fresh, ticket = rng.normal(5200, 700), rng.normal(6, 2), rng.normal(0.55, 0.08), rng.normal(900, 150)
        rows.append([round(max(spend, 200), 2), round(max(visits, 1), 1),
                     round(min(max(fresh, 0.05), 0.85), 3), round(max(ticket, 50), 2)])
    write_csv("supermarket_customers.csv", rows,
              ["monthly_spend_ttd", "visits_per_month", "fresh_share", "avg_ticket_ttd"])


def caribbean_country_facts_json():
    facts = {
        "Jamaica": [
            "Home of Blue Mountain Coffee.",
            "Usain Bolt is the fastest sprinter in recorded history.",
            "Maroons signed a treaty with the British in 1739.",
            "Independence from Britain on 6 August 1962.",
        ],
        "Trinidad and Tobago": [
            "Birthplace of the steel pan.",
            "Largest oil and gas producer in CARICOM.",
            "Independence on 31 August 1962.",
            "Scarlet Ibis is the national bird of Trinidad.",
        ],
        "Barbados": [
            "Became a republic on 30 November 2021.",
            "Mount Gay Rum has operated since 1703.",
            "Capital is Bridgetown, a UNESCO site.",
            "Currency BBD is pegged 2:1 to USD.",
        ],
        "Bahamas": [
            "An archipelago of about 700 islands and cays.",
            "Junkanoo is its main cultural festival.",
            "Currency BSD is pegged 1:1 to USD.",
            "Independence on 10 July 1973.",
        ],
        "Haiti": [
            "First independent Black republic, 1804.",
            "Official languages: Kreyol and French.",
            "Citadelle Laferrière is the largest fortress in the Americas.",
        ],
        "Dominican Republic": [
            "Santo Domingo is the oldest continuously inhabited European founded city in the Americas.",
            "Pico Duarte is the highest peak in the Caribbean.",
            "Merengue is the national music.",
        ],
        "Cuba": ["Largest island in the Caribbean.", "Capital is Havana.", "Birthplace of son, mambo, and salsa."],
        "Puerto Rico": ["United States territory since 1898.", "El Yunque is a US National Forest.", "Home of reggaeton."],
        "Guyana": ["Only English speaking country in South America.", "Kaieteur Falls is among the most powerful waterfalls."],
        "Suriname": ["Smallest sovereign nation in South America.", "Paramaribo is a UNESCO site."],
        "Belize": ["Hosts the second largest barrier reef in the world.", "Garifuna culture is UNESCO recognised."],
        "Antigua and Barbuda": ["Famous for 365 beaches.", "Nelson's Dockyard is a UNESCO site."],
        "Dominica": [
            "Known as the Nature Isle.",
            "Home of the Kalinago, the only remaining pre-Columbian indigenous population in the Eastern Caribbean.",
            "Boiling Lake is the world's second largest hot lake.",
        ],
        "Grenada": ["Known as the Spice Isle.", "Underwater Sculpture Park near Saint George's.", "Nutmeg and mace exporter."],
        "Saint Kitts and Nevis": ["Smallest sovereign state in the Western Hemisphere.", "Brimstone Hill Fortress is a UNESCO site."],
        "Saint Lucia": [
            "Home to the Pitons, a UNESCO World Heritage Site.",
            "Two Nobel laureates: Sir Arthur Lewis and Derek Walcott.",
            "Soufrière has a drive in volcano.",
        ],
        "Saint Vincent and the Grenadines": ["La Soufrière erupted in 2021.", "Grenadines are 32 islands."],
        "Aruba": ["Papiamento is widely spoken.", "Outside the hurricane belt."],
        "Curaçao": ["Willemstad is a UNESCO site.", "Curaçao liqueur originates here."],
        "Cayman Islands": ["Major hedge fund and insurance jurisdiction.", "Seven Mile Beach is world famous."],
        "Turks and Caicos Islands": ["About 40 islands and cays.", "Grace Bay is among the world's best beaches."],
        "British Virgin Islands": ["Sailing destination via the Sir Francis Drake Channel.", "Offshore financial centre."],
        "United States Virgin Islands": ["Three main islands: Saint Thomas, Saint Croix, Saint John.", "US territory since 1917."],
        "Bermuda": ["Pink sand beaches due to crushed red foram skeletons.", "Major reinsurance hub.", "Gombey dance combines African and British military traditions."],
    }
    (OUT / "caribbean_country_facts.json").write_text(json.dumps(facts, indent=2))
    print(f"wrote {OUT / 'caribbean_country_facts.json'}")


def datasets_readme():
    text = """# Datasets

A mix of synthetic Caribbean datasets generated by `scripts/generate_datasets.py`
plus pointers to real public sources.

## Files

| File | Description | Source |
|------|-------------|--------|
| saint_lucia_rainfall.csv | Monthly rainfall and temperature, 2010 to 2025 | Synthetic |
| caribbean_mangoes.csv | Mango physical measurements by variety | Synthetic |
| barbados_arrivals.csv | Monthly stayover arrivals, 2014 to 2025 | Synthetic (pattern based) |
| tourism_reviews.csv | Short tourism reviews across the region | Hand crafted |
| remittance_transactions.csv | Transaction features and a suspicious flag | Synthetic |
| yam_yield.csv | Yam yields by parish | Synthetic |
| market_prices_weekly.csv | Weekly produce prices, Coronation Market | Synthetic |
| atlantic_storms.csv | Storm features and peak wind | Synthetic |
| sea_level_monthly.csv | Monthly sea level at a station | Synthetic |
| sst_anomaly.csv | Monthly sea surface temperature anomaly by site | Synthetic |
| caribbean_dialect_phrases.csv | Phrases by country | Hand crafted |
| supermarket_customers.csv | Trinidad supermarket customer features | Synthetic |
| caribbean_country_facts.json | Facts used by the RAG demo | Hand crafted |

## Regenerate

```bash
python scripts/generate_datasets.py
```

## Real data sources to graduate to

- CARICOM Regional Statistics
- STATIN, Central Statistical Office, Barbados Statistical Service
- NOAA HURDAT2 (Atlantic hurricane database)
- NOAA Coral Reef Watch
- World Bank Open Data
- Caribbean Tourism Organization
- Caribbean Community Climate Change Centre (5Cs)
"""
    (OUT / "README.md").write_text(text)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    saint_lucia_rainfall()
    caribbean_mangoes()
    barbados_arrivals()
    tourism_reviews()
    remittance_transactions()
    yam_yield()
    market_prices_weekly()
    atlantic_storms()
    sea_level_monthly()
    sst_anomaly()
    caribbean_dialect_phrases()
    supermarket_customers()
    caribbean_country_facts_json()
    datasets_readme()


if __name__ == "__main__":
    main()
