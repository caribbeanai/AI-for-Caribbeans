# Lesson 2, Classification

Classification predicts a category. Spam or not. Fraud or legit. Mango type. Storm category.

## Binary versus multiclass

Binary: two classes. Multiclass: three or more.

## Common models

- Logistic regression. Despite the name it is for classification. Great baseline.
- Decision trees and random forests.
- Gradient boosting, XGBoost or LightGBM. Often wins on tabular data.
- Neural networks for very large data.

## Metrics, beyond accuracy

Accuracy can lie. If 99 percent of transactions are legit, a model that always says "legit" is 99 percent accurate and 100 percent useless.

Better metrics:
- Precision, of those flagged fraud, how many really are.
- Recall, of all true fraud, how many we caught.
- F1 score, the harmonic mean of precision and recall.
- ROC AUC, ranking quality across thresholds.

## Caribbean example

Classifying whether a remittance is suspicious from sender country, amount, time of day, and account age. See `remittance_fraud.py`.
