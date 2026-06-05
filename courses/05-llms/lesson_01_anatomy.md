# Lesson 1, Anatomy of an LLM

A modern LLM has four working parts.

## 1. Tokenizer

Splits text into subword units. "Bridgetown" might be one token. "Speightstown" might be three.

Implication: words common in mainstream English are cheap. Rare Caribbean place names and Kreyol words may use many tokens, costing more and reducing quality.

## 2. The model

A stack of Transformer layers, often 30 to 120 deep. Billions of parameters. Trained to predict the next token.

## 3. Training data

Public web text plus curated corpora plus human feedback. Most models have thin Caribbean dialect data. This is a known limitation.

## 4. Inference settings

- Temperature, randomness.
- Top-p, sampling pool.
- Max tokens, output length.
- Stop sequences, where to end.
- System prompt, the persistent instructions.

## What is a context window

The total tokens the model can read in one call, prompt plus output. Today, 200,000 to 1,000,000 tokens is common. That is whole books at a time.

## Pricing intuition

Most providers charge per million input and output tokens. Input is cheaper than output. Caching repeated prompts can drop costs significantly.
