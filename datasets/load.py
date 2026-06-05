"""
Single entry point for loading every dataset in this repo.

Usage:

    from datasets.load import load
    df = load("saint_lucia_rainfall")
    facts = load("caribbean_country_facts")  # returns dict for JSON

Pass `list_datasets()` to see what is available.

Author: Adrian Dunkley
"""

from pathlib import Path
import json

try:
    import pandas as pd
except ImportError:
    pd = None


DATA_DIR = Path(__file__).resolve().parent


REGISTRY = {
    # name -> (filename, kind, short_description, columns, caribbean_context)
    "saint_lucia_rainfall": (
        "saint_lucia_rainfall.csv", "csv",
        "Monthly rainfall and mean temperature for Saint Lucia, 2010 to 2025.",
        ["month", "year", "mean_temp_c", "rainfall_mm"],
        "Wet season runs June to November. Hurricane Tomas (2010) and Matthew (2016) shaped recent extremes.",
    ),
    "caribbean_mangoes": (
        "caribbean_mangoes.csv", "csv",
        "Physical measurements for four mango varieties common across the Caribbean.",
        ["length_cm", "width_cm", "weight_g", "sweetness_brix", "variety"],
        "Varieties: Julie, East Indian, Bombay, Number Eleven. Julie is small, round, very sweet.",
    ),
    "barbados_arrivals": (
        "barbados_arrivals.csv", "csv",
        "Monthly stayover arrivals to Barbados.",
        ["date", "arrivals"],
        "High season Dec to Mar drives most volume. The 2020 dip captures the COVID closure.",
    ),
    "tourism_reviews": (
        "tourism_reviews.csv", "csv",
        "Short tourism reviews from across the Caribbean.",
        ["id", "review", "label"],
        "Mixes resorts, tours, and food experiences from at least a dozen islands.",
    ),
    "remittance_transactions": (
        "remittance_transactions.csv", "csv",
        "Synthetic remittance transactions with a suspicious flag for binary classification.",
        ["amount_usd", "sender_country_risk", "receiver_account_age_days", "hour_of_day",
         "channel_atm", "channel_branch", "channel_online", "is_suspicious"],
        "Reflects USD inbound to JMD style currencies, late night and online channels carry more risk.",
    ),
    "yam_yield": (
        "yam_yield.csv", "csv",
        "Yam yield per acre by Jamaican parish.",
        ["parish", "rainfall_mm", "fertiliser_kg_per_acre", "area_acres", "yield_kg_per_acre"],
        "Top yam parishes: Trelawny, Saint Mary, Manchester, Saint Ann.",
    ),
    "market_prices_weekly": (
        "market_prices_weekly.csv", "csv",
        "Weekly produce prices for Coronation Market style items.",
        ["date", "item", "price_jmd_per_lb"],
        "Includes a scotch bonnet shock event to teach anomaly detection.",
    ),
    "atlantic_storms": (
        "atlantic_storms.csv", "csv",
        "Synthetic Atlantic storm features and peak wind.",
        ["init_wind_mph", "init_pressure_mb", "sst_c", "shear_kt", "lat", "lon", "peak_wind_mph"],
        "Storms initialised in classic Cape Verde and Caribbean Sea bands.",
    ),
    "sea_level_monthly": (
        "sea_level_monthly.csv", "csv",
        "Monthly sea level at a representative Caribbean tide station.",
        ["year", "month", "level_mm"],
        "Trend close to 3.4 mm per year, plus a seasonal cycle.",
    ),
    "sst_anomaly": (
        "sst_anomaly.csv", "csv",
        "Monthly sea surface temperature anomaly at five reef sites.",
        ["year", "month", "site", "sst_anomaly_c"],
        "Cayman Reefs, Belize Barrier, Tobago Cays, Bonaire Marine Park, Saba Bank.",
    ),
    "caribbean_dialect_phrases": (
        "caribbean_dialect_phrases.csv", "csv",
        "Dialect phrases with the country they come from.",
        ["country", "phrase"],
        "Patois, Bajan, Trini, Kwéyòl, Kreyol, Papiamento, Sranan, more.",
    ),
    "supermarket_customers": (
        "supermarket_customers.csv", "csv",
        "Trinidad supermarket customer features for segmentation.",
        ["monthly_spend_ttd", "visits_per_month", "fresh_share", "avg_ticket_ttd"],
        "Four hidden segments: weekly family, weekend bulk, daily topup, premium.",
    ),
    "hotel_bookings_caribbean": (
        "hotel_bookings_caribbean.csv", "csv",
        "Hotel bookings across Caribbean destinations with cancellation labels.",
        ["destination", "lead_time_days", "nights", "guests", "channel", "rate_usd", "is_cancelled"],
        "Channels reflect Booking, Expedia, direct, agent.",
    ),
    "cricket_matches_wi": (
        "cricket_matches_wi.csv", "csv",
        "West Indies cricket match results across formats.",
        ["date", "format", "opponent", "venue", "wi_runs", "opp_runs", "wi_wickets", "opp_wickets", "result"],
        "Spans Tests, ODIs, T20Is. Useful for sports analytics.",
    ),
    "remitter_diaspora_panel": (
        "remitter_diaspora_panel.csv", "csv",
        "Monthly remittance volume by sending country and Caribbean destination.",
        ["year", "month", "from_country", "to_country", "volume_usd_millions"],
        "USA, Canada, UK to Jamaica, Haiti, Dominican Republic, Guyana, Trinidad, more.",
    ),
    "fishing_landings": (
        "fishing_landings.csv", "csv",
        "Daily fish landings at small Caribbean ports.",
        ["date", "port", "species", "weight_kg", "price_per_kg_usd"],
        "Snapper, lobster, kingfish, mahi mahi, lionfish across OECS ports.",
    ),
    "solar_irradiance": (
        "solar_irradiance.csv", "csv",
        "Hourly solar irradiance for a residential PV planning study.",
        ["timestamp", "site", "ghi_w_m2", "temperature_c", "cloud_cover_pct"],
        "Sites in Kingston, Bridgetown, Castries.",
    ),
    "school_attendance": (
        "school_attendance.csv", "csv",
        "Daily school attendance with weather and term context.",
        ["date", "school", "parish", "attendance_pct", "rainfall_mm", "is_exam_term"],
        "Useful for predicting attendance dips and intervention planning.",
    ),
    "health_clinic_visits": (
        "health_clinic_visits.csv", "csv",
        "Clinic visits with reason and parish, useful for public health forecasting.",
        ["date", "parish", "reason", "visits"],
        "Reasons: dengue suspect, hypertension, diabetes, prenatal, injury.",
    ),
    "carnival_attendance": (
        "carnival_attendance.csv", "csv",
        "Daily attendance across Caribbean Carnivals.",
        ["country", "year", "event_day", "attendance"],
        "Trinidad, Barbados Crop Over, Saint Lucia, Saint Vincent Vincy Mas, Grenada Spicemas.",
    ),
    "real_estate_listings": (
        "real_estate_listings.csv", "csv",
        "Residential listings across Caribbean cities.",
        ["city", "neighbourhood", "beds", "baths", "sqft", "price_local", "currency"],
        "New Kingston, Westmoorings, Christ Church, Cap Estate, Bavaro.",
    ),
    "caribbean_country_facts": (
        "caribbean_country_facts.json", "json",
        "Facts per country, used by the RAG tutorial.",
        ["country -> [facts...]"],
        "Curated hand written facts.",
    ),
}


def list_datasets():
    """Return a list of dataset names available in this repo."""
    return sorted(REGISTRY.keys())


def describe(name):
    """Return a dict describing a single dataset."""
    if name not in REGISTRY:
        raise KeyError(f"Unknown dataset: {name}. See list_datasets().")
    filename, kind, desc, cols, ctx = REGISTRY[name]
    return {
        "name": name,
        "filename": filename,
        "kind": kind,
        "description": desc,
        "columns": cols,
        "caribbean_context": ctx,
        "path": str(DATA_DIR / filename),
    }


def load(name):
    """Load a dataset by name. Returns a pandas DataFrame for csv, or a dict for json."""
    if name not in REGISTRY:
        raise KeyError(f"Unknown dataset: {name}. See list_datasets().")
    filename, kind, *_ = REGISTRY[name]
    path = DATA_DIR / filename
    if kind == "csv":
        if pd is None:
            raise ImportError("Install pandas to load csv datasets.")
        return pd.read_csv(path)
    if kind == "json":
        return json.loads(path.read_text())
    raise ValueError(f"Unknown kind: {kind}")


if __name__ == "__main__":
    for n in list_datasets():
        info = describe(n)
        print(f"- {n:32} {info['description']}")
