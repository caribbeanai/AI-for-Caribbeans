# Lesson 6, Pitfalls and leakage

The number one reason a model that "worked in training" fails in production: data leakage.

## Common leaks

- Using a feature that is only known after the outcome. Example: using "payment received" when predicting "will this invoice be paid".
- Joining on a date that includes the future.
- Scaling using the full dataset before splitting. Always fit the scaler on train only.
- Target encoding without proper cross fitting.

## Other pitfalls

- Class imbalance ignored. A 99 percent legit class will hide your model's failures on the 1 percent that matters.
- Concept drift. The world changes. Tourist arrivals after a hurricane do not follow last year's patterns. Retrain on rolling windows.
- Survivorship bias. If you only train on borrowers who got loans, you will never learn about those who would have repaid if approved.
- Snooping the test set. Even one accidental peek invalidates your evaluation.

## A pre-launch checklist

1. Have I tested on a holdout the model has never seen.
2. Have I checked performance on segments that matter (parish, gender, age).
3. Is there a baseline I can beat clearly.
4. Do I have a plan to monitor performance in production.
5. Do I have a rollback plan when performance drops.
