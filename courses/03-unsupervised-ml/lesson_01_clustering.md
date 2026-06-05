# Lesson 1, Clustering

Clustering groups points so that points in the same group are similar to each other and different from points in other groups.

## K-means

Pick k. Randomly place k centres. Assign each point to the closest centre. Move the centre to the mean of its points. Repeat until stable.

Pros: fast, simple, scales.
Cons: needs k upfront, assumes round clusters of similar size, sensitive to scaling.

## Choosing k

- Elbow method on inertia.
- Silhouette score.
- Business sense. Three customer segments are easier to action than thirty.

## When k-means is the wrong tool

- Dense and sparse regions: use DBSCAN.
- Hierarchical structure: use agglomerative clustering.
- Manifold or non-convex shapes: use HDBSCAN, often with UMAP.

## Caribbean example

Segment 5,000 supermarket customers in Port of Spain by basket size, visits per month, share of fresh produce, and average ticket. Three clusters often appear: weekly families, weekend bulk buyers, daily top up shoppers. Each gets a different marketing approach.
