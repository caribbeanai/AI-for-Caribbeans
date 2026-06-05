# Dataset Catalog

A single page index of every dataset in this repository. All datasets are synthetic but built on realistic Caribbean patterns: hurricane seasonality, tourism peaks around Christmas and Crop Over, dengue spikes in wet months, remittance highs in December, currency pegs, parish geography, dialect samples by country.

## How to load any dataset

```python
from datasets.load import load, list_datasets, describe

print(list_datasets())          # see what is available
print(describe("yam_yield"))    # info on one dataset
df = load("hotel_bookings_caribbean")
facts = load("caribbean_country_facts")  # returns dict, not DataFrame
```

Or read the file directly:

```python
import pandas as pd
df = pd.read_csv("datasets/saint_lucia_rainfall.csv")
```

## Index

### Climate and environment

| Dataset | Rows | Use for |
|--------|------|--------|
| `saint_lucia_rainfall` | 192 | Monthly rainfall regression, seasonality |
| `atlantic_storms` | 400 | Hurricane intensity prediction |
| `sea_level_monthly` | 432 | Linear trend, climate communication |
| `sst_anomaly` | 480 | Reef bleaching risk, anomaly detection |
| `solar_irradiance` | ~14k | Residential PV sizing, time series |

### Tourism

| Dataset | Rows | Use for |
|--------|------|--------|
| `barbados_arrivals` | 144 | Monthly arrivals forecasting |
| `tourism_reviews` | 35 | Sentiment, topic modelling |
| `hotel_bookings_caribbean` | 5,000 | Cancellation classification, segmentation |
| `carnival_attendance` | 90 | Event analytics, capacity planning |

### Finance

| Dataset | Rows | Use for |
|--------|------|--------|
| `remittance_transactions` | 3,000 | Fraud detection, imbalanced classification |
| `remitter_diaspora_panel` | 2,880 | Panel data, monthly diaspora flows |
| `real_estate_listings` | 1,200 | Multi currency pricing, regression |

### Agriculture and food

| Dataset | Rows | Use for |
|--------|------|--------|
| `caribbean_mangoes` | 240 | Multiclass classification |
| `yam_yield` | 600 | Yield regression, parish effects |
| `market_prices_weekly` | 624 | Anomaly detection, price forecasting |
| `fishing_landings` | ~19k | Port level fisheries analytics |

### Society and language

| Dataset | Rows | Use for |
|--------|------|--------|
| `supermarket_customers` | 1,200 | Clustering, segmentation |
| `caribbean_dialect_phrases` | 30 | Dialect clustering, language ID |
| `school_attendance` | 1,100 | Attendance prediction, dropout risk |
| `health_clinic_visits` | 13,500 | Dengue early warning, public health |
| `cricket_matches_wi` | 224 | Sports analytics |
| `caribbean_country_facts` (JSON) | 24 countries | RAG over local facts |

## Regenerate everything

```bash
python scripts/generate_datasets.py
python scripts/generate_extra_datasets.py
```

## Add your own

1. Add a generator function in `scripts/generate_extra_datasets.py` or a new file in `scripts/`.
2. Register the dataset in `datasets/load.py` REGISTRY so others can use `load("your_name")`.
3. Note the Caribbean context in the registry, not just the columns.

## Real public sources to graduate to

When you outgrow the synthetic versions, point your code at real data:

- CARICOM Regional Statistics: https://caricomstats.org
- Statistical Institute of Jamaica (STATIN)
- Central Statistical Office of Trinidad and Tobago
- Barbados Statistical Service
- World Bank Open Data, filter by Caribbean countries
- NOAA HURDAT2 (Atlantic hurricane database)
- NOAA Coral Reef Watch
- Caribbean Tourism Organization
- Caribbean Community Climate Change Centre (5Cs), Belmopan
- IADB and ECLAC data portals
- Open Caribbean Maps (OSM Caribbean), https://www.openstreetmap.org
- World Resources Institute Aqueduct (water risk by basin)
- Copernicus Climate Data Store for satellite climate data
