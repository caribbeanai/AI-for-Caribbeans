# Supervised ML: Scenarios

Six end to end scenarios. Each maps to a dataset in `datasets/` and a starter script.

## Scenario 1: A hotel in Negril wants to cut cancellations

**Business question:** Of the bookings on the next 90 day pace, which are most likely to cancel?

**Dataset:** `hotel_bookings_caribbean` (5,000 rows, ten destinations including Negril and Montego Bay).

**Starter:**

```python
from datasets.load import load
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, classification_report
import pandas as pd

df = load("hotel_bookings_caribbean")
df = pd.get_dummies(df, columns=["destination", "channel"], drop_first=True)
y = df["is_cancelled"]
X = df.drop(columns=["is_cancelled"])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model = HistGradientBoostingClassifier(max_iter=400, random_state=42).fit(X_train, y_train)
probs = model.predict_proba(X_test)[:, 1]
print(f"ROC AUC: {roc_auc_score(y_test, probs):.3f}")
print(classification_report(y_test, model.predict(X_test)))
```

**Decisions to make:** What probability threshold triggers a "high risk" tag in the PMS? What action follows: a phone call, a flexible date offer, or a non refundable upgrade discount?

## Scenario 2: A yam farmer in Trelawny needs a yield estimate before harvest

**Business question:** Given rainfall to date, fertiliser used, and acres planted, what yield should I plan for?

**Dataset:** `yam_yield`.

**Starter:** see `courses/02-supervised-ml/lesson_05_trees.md`. Use a HistGradientBoostingRegressor with parish one hot encoded.

**Decisions:** With a forecast yield, the farmer plans labour, transport, and at which Coronation Market week to sell.

## Scenario 3: Saint Lucia Met Office wants a rainfall sanity check

**Business question:** Given a candidate forecast for next month, does it look reasonable against history?

**Dataset:** `saint_lucia_rainfall`.

**Starter:** `courses/02-supervised-ml/rainfall_saint_lucia.py`.

**Decisions:** If the forecast is more than 3 standard deviations from historical median for that month, escalate to a senior forecaster.

## Scenario 4: A remittance provider wants to flag suspicious transactions in real time

**Business question:** Block, hold for review, or release?

**Dataset:** `remittance_transactions`.

**Starter:** `courses/02-supervised-ml/remittance_fraud.py`.

**Decisions:** Set the threshold per cost of false positive (a frozen valid transfer) versus false negative (an actual fraud). Track precision and recall by sender country and channel.

## Scenario 5: A Coronation Market vendor wants to anticipate price spikes for scotch bonnet

**Business question:** When is the next likely scotch bonnet price spike, and by how much?

**Dataset:** `market_prices_weekly`.

**Approach:** Combine simple time series features (lag 1, lag 4, year on year) with a small gradient boosted model.

**Decisions:** Buy and store an extra week of supply before a forecasted spike, then sell on the spike day. The vendor's margin lives in the timing.

## Scenario 6: A Bridgetown real estate agent wants comparable listings

**Business question:** What is a fair asking price for a 3 bed, 2 bath, 1,400 sqft house in Christ Church?

**Dataset:** `real_estate_listings`.

**Starter:**

```python
from datasets.load import load
df = load("real_estate_listings")
christ_church = df[df["neighbourhood"] == "Christ Church"]
# fit a HistGradientBoostingRegressor on beds, baths, sqft -> price_local
```

**Decisions:** Set listing price 5 percent above model estimate as a negotiation anchor. If it does not sell in 30 days, drop to model estimate.

## Capstone

Pick any scenario, write the one page case study (see `capstone_template.md`), and present it to a real audience: a market vendor, a hotel manager, a teacher. Their reaction tells you whether the model matters.
