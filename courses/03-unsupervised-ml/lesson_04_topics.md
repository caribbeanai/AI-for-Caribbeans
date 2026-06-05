# Lesson 4, Topic modelling for Caribbean text

Given a pile of text, find the underlying themes.

## Classical approach, LDA

Latent Dirichlet Allocation. Treats each document as a mix of topics, and each topic as a mix of words. Old but useful.

## Modern approach, BERTopic and embeddings plus clustering

1. Encode each document with a sentence embedding model.
2. Reduce dimensions with UMAP.
3. Cluster with HDBSCAN.
4. Extract characteristic words per cluster.

This works much better on short, informal Caribbean text than LDA does.

## Caribbean specific cautions

- Stop word lists often miss our common words. Add: "wah", "gwaan", "lyme", "dey", "ah", "gyal", "fella" to dialect aware stop word lists where appropriate.
- Mixed code text is common. A review may switch between English and Kreyol mid sentence. Use multilingual embeddings.
- Names of dishes, festivals, and places matter. Do not strip them as noise. Curry goat, doubles, callaloo, bake and shark, mauby. They are signal.
