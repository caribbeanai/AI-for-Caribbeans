# Lesson 5, Transfer learning

Almost no one trains a useful image, audio, or text model from scratch in 2026. You start with a model someone else trained on a giant dataset and adapt it.

## Strategy 1, feature extraction

Freeze the backbone, train only a small new head. Fast, works with small data.

## Strategy 2, fine tuning

Unfreeze part or all of the backbone, train with a small learning rate. Better accuracy, needs more data and compute.

## Strategy 3, adapters and LoRA

Add small trainable modules to a frozen model. Standard for LLMs.

## How much data do I need

- Image classification, transfer learning: 100 to 500 images per class is a starting point.
- Audio classification: similar.
- Text classification with embeddings plus a classifier head: 50 to 500 examples per class often works.

## A weekend project plan

1. Friday evening, collect 600 images, 200 per class.
2. Saturday morning, label them in a tool like Label Studio.
3. Saturday afternoon, train a transfer learning model.
4. Sunday morning, evaluate and write up.
