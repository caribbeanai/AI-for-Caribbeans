# Scripts

Utility scripts used to build and maintain the repository.

| Script | Purpose |
|--------|---------|
| `generate_country_profiles.py` | Generate `countries/<slug>/README.md` files from a single source of truth |
| `generate_datasets.py` | Generate the synthetic datasets under `datasets/` |
| `check_repo_health.py` | Sanity check: count files, verify generated content |

Run from the repo root:

```bash
python scripts/generate_country_profiles.py
python scripts/generate_datasets.py
python scripts/check_repo_health.py
```
