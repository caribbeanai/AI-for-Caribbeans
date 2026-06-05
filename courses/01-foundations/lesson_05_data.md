# Lesson 5, Data, the fuel

A great model on bad data is a fast car with bad fuel. It goes nowhere.

## What good data looks like

- Relevant to the question.
- Enough volume for the task.
- Recent enough to reflect the world today.
- Cleaned. No stray characters, consistent units, sensible ranges.
- Labelled, if you are doing supervised learning.
- Free of personal data leakage.

## Where to get Caribbean data

- CARICOM Regional Statistics, https://caricomstats.org
- Statistical Institute of Jamaica (STATIN)
- Central Statistical Office of Trinidad and Tobago
- Barbados Statistical Service
- Caribbean Community Climate Change Centre (5Cs), Belmopan
- NOAA Atlantic hurricane archives
- Caribbean Tourism Organization
- World Bank Open Data, filter by Caribbean countries
- This repo's [datasets folder](../../datasets), which includes curated and synthetic Caribbean data

## A practical data hygiene checklist

1. Save the raw download untouched.
2. Make a copy for cleaning.
3. Document units. Is rainfall in mm or inches? Is currency JMD or USD?
4. Check for nulls. Are they missing or zero?
5. Look at the extremes. Maximum and minimum values often reveal data errors.
6. Plot it before modelling it. Always plot it.
7. Keep a data dictionary. Every column, what it means, units, source.

## Caribbean specific cautions

- Place names vary. "St. James" can mean a Jamaica parish, a Barbados parish, or a Trinidad town. Disambiguate before joining datasets.
- Population figures can be five or six years stale in some islands. Adjust your conclusions.
- Currency conversions need a dated exchange rate. The JMD has drifted; do not assume one rate across years.
