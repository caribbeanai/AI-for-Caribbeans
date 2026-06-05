# Course 02, Supervised Machine Learning

Predict things from labelled examples. By the end you can build, evaluate, and explain a real model.

## Lessons

1. [Regression, predicting numbers](lesson_01_regression.md)
2. [Classification, predicting categories](lesson_02_classification.md)
3. [Feature engineering for Caribbean data](lesson_03_features.md)
4. [Evaluation: accuracy, precision, recall, MAE, MAPE](lesson_04_evaluation.md)
5. [Tree based models and why they win on tabular data](lesson_05_trees.md)
6. [Pitfalls and leakage](lesson_06_pitfalls.md)

## Scenarios

Six end to end Caribbean scenarios live in [scenarios.md](scenarios.md), each mapped to a dataset and a starter script.

## Datasets

All datasets used here come from `datasets/`. See the full index: [../../datasets/CATALOG.md](../../datasets/CATALOG.md). Load any of them with `from datasets.load import load`.

## Code

- [rainfall_saint_lucia.py](rainfall_saint_lucia.py), predict monthly rainfall.
- [mango_classifier.py](mango_classifier.py), Julie versus East Indian.
- [tourist_arrivals.py](tourist_arrivals.py), forecast arrivals to Barbados.
- [remittance_fraud.py](remittance_fraud.py), classify suspicious transactions.
- [hotel_cancellation.py](hotel_cancellation.py), predict cancellations across ten Caribbean destinations.
- [real_estate_pricing.py](real_estate_pricing.py), price listings in JMD, TTD, BBD, XCD, DOP, USD.

## Capstone

Pick one Caribbean problem with at least 200 rows of data, build a supervised model, write a one page case study with business impact. Templates in [capstone_template.md](capstone_template.md).
