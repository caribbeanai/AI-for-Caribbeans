# Lesson 2, Dimensionality reduction

Many features, but few really matter. Reducing dimensions makes data easier to visualise and often helps downstream models.

## PCA

Linear projection that captures the most variance. Use for compression, visualisation, and de-noising.

## UMAP and t-SNE

Non linear. Great for visualising clusters in 2D. Do not use the resulting coordinates as features in a downstream model unless you understand the trade-offs.

## When to use what

- PCA before fitting a slow model: keep 95 percent of variance.
- UMAP for plotting clusters in a slide deck.
- Autoencoders for image or audio compression.

## Caution

UMAP and t-SNE move points around in ways that look meaningful but exaggerate small differences. Treat the plot as a hint, not a truth.
