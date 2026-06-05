# Lesson 5, Tree based models

For tabular data with mixed types and missing values, gradient boosted trees usually win. They handle non-linear relationships, do not need scaling, and produce strong baselines fast.

## Decision tree, the building block

Split the data on the feature and threshold that most reduces impurity. Repeat on each branch. Stop when depth or sample count is small.

## Random forest

Many trees, each trained on a random subset of rows and features. Average their predictions. Reduces variance.

## Gradient boosting

Build trees one at a time, each correcting the errors of the previous ones. Implementations to know:

- scikit-learn's HistGradientBoosting
- XGBoost
- LightGBM
- CatBoost, strong on categoricals

## A baseline you can copy

```python
from sklearn.ensemble import HistGradientBoostingRegressor

model = HistGradientBoostingRegressor(
    max_iter=300,
    learning_rate=0.05,
    max_depth=6,
    random_state=42,
)
model.fit(X_train, y_train)
preds = model.predict(X_test)
```

## Feature importance, with caution

Gradient boosters expose feature importances. They are useful but misleading when features are correlated. For trustworthy attribution, use permutation importance or SHAP values.
