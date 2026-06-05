# Datasets

This folder is the single home for every dataset used across the courses, applications, and tutorials in this repository.

**Start here:** [CATALOG.md](CATALOG.md) is the full index with context, row counts, and one line use cases.

## How to use

Programmatic loading is supported via a tiny helper:

```python
from datasets.load import load, list_datasets, describe

names = list_datasets()
print(names)

info = describe("hotel_bookings_caribbean")
print(info)

df = load("hotel_bookings_caribbean")
```

Or read the CSV files directly with pandas. Every dataset is plain UTF-8 CSV or JSON.

## Regenerate

These datasets are synthetic but built on plausible Caribbean patterns. You can regenerate them at any time:

```bash
python scripts/generate_datasets.py
python scripts/generate_extra_datasets.py
```

Random seeds are fixed so the output is reproducible.

## Honesty about synthetic data

We use synthetic data so we can teach in public without fragility around licensing or stale public data. Patterns reflect regional realities: hurricane seasonality, currency pegs, tourism peaks, dengue spikes in wet months, parish level variation. Do not use these files for research claims. When you are ready to graduate, point your pipeline at the real sources listed in CATALOG.md.
