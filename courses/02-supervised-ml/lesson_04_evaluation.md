# Lesson 4, Evaluation

## Always hold out

Split your data into train, validation, and test. Touch the test set only at the very end. If you peek, you are fooling yourself.

A simple split: 70 train, 15 validation, 15 test. For time series, split by date, not at random.

## Regression metrics, choose one and report it

- MAE in real units. Easy to communicate.
- RMSE when large errors matter more.
- MAPE when scales vary. Be careful when actuals can be zero or near zero.

## Classification metrics

- Confusion matrix. Always look at it.
- Precision and recall per class.
- F1 per class for imbalanced problems.
- ROC AUC and PR AUC.

## Calibration

A predicted probability of 0.8 should be right roughly 80 percent of the time. Plot a reliability diagram. Use Platt scaling or isotonic regression to fix it.

## Beyond metrics, the business question

A model with 0.95 ROC AUC that recommends bad loans is still a bad model. Translate metrics into dollars.

Example: a fraud model with recall 0.6 at precision 0.8 saves X transactions worth Y dollars per month, at the cost of Z false flags that take W minutes each to review.
