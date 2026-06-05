# Lesson 1, Regression

Regression predicts a number. House price, rainfall, GDP, hotel occupancy.

## The simplest model, linear regression

The model assumes the output is a weighted sum of the inputs.

`y = w1 * x1 + w2 * x2 + ... + b`

Training finds the weights that minimise squared error on the training data.

## Run the example

```bash
python courses/02-supervised-ml/rainfall_saint_lucia.py
```

It predicts monthly rainfall in millimetres from month number, year, and average temperature. The data is in `datasets/saint_lucia_rainfall.csv`.

## When to use linear regression

- Small datasets.
- You want easy interpretation, the weights tell a story.
- The relationship is roughly linear after sensible transformations.

## When to upgrade

- Use polynomial features for curves.
- Use gradient boosted trees for tabular data with many features.
- Use neural networks for very large datasets with complex relationships.

## Evaluation

For regression we use:
- Mean Absolute Error, MAE, in the units of the target.
- Root Mean Squared Error, RMSE, punishes large misses.
- Mean Absolute Percentage Error, MAPE, useful when the target spans orders of magnitude.
