# Unsupervised ML: Scenarios

## Scenario 1: A Trinidad supermarket chain wants better promotions

**Business question:** Which customer groups exist, and what offer fits each?

**Dataset:** `supermarket_customers`.

**Starter:** `courses/03-unsupervised-ml/customer_segmentation.py`.

**Action:** weekly families get a Sunday newspaper coupon, weekend bulk buyers get an early opening hour notice, daily top up shoppers get a points loyalty card with low thresholds, premium customers get private wine tastings.

## Scenario 2: A Bridgetown hotel wants the themes hidden in 2,000 reviews

**Business question:** What did guests really care about last season?

**Dataset:** `tourism_reviews`. For real volume, scrape your own.

**Starter:** `courses/03-unsupervised-ml/tourist_review_topics.py`.

**Action:** invest where the negative themes cluster (slow service at the bar, broken AC) and double down on the positive ones (location, breakfast).

## Scenario 3: A Caribbean language project wants dialect groups for testing data

**Business question:** Group phrases by surface similarity so we can sample evenly when building a multilingual eval set.

**Dataset:** `caribbean_dialect_phrases`.

**Starter:** `courses/03-unsupervised-ml/dialect_clustering.py`.

**Action:** sample N phrases from each cluster for human review before adding to your eval corpus.

## Scenario 4: A fisheries officer wants to spot illegal landings

**Business question:** Which port days look unlike the rest?

**Dataset:** `fishing_landings`.

**Starter:**

```python
from datasets.load import load
from sklearn.ensemble import IsolationForest
df = load("fishing_landings")
agg = df.groupby(["date", "port"])[["weight_kg", "price_per_kg_usd"]].sum().reset_index()
X = agg[["weight_kg", "price_per_kg_usd"]]
flags = IsolationForest(contamination=0.02, random_state=42).fit_predict(X)
print(agg[flags == -1].head())
```

**Action:** human review. Anomaly does not equal crime, but it is where attention pays off.

## Scenario 5: A school district wants schools with similar attendance patterns

**Business question:** Cluster schools so we can run pilots on similar groups.

**Dataset:** `school_attendance`.

**Approach:** aggregate to one row per school (mean attendance, attendance volatility, rain sensitivity), then KMeans with k between 3 and 5.

**Action:** pilot an intervention in one cluster, control in another, measure the effect after one term.

## Scenario 6: An e commerce founder in Aruba wants to find new market segments

**Business question:** Which customer behaviours hide in our purchase history?

**Dataset:** synthetic supermarket data is a stand in. Bring your real data when you have it.

**Action:** name your clusters with care. A name like "the weekend wine buyers" is far more useful in a meeting than "cluster 2".
