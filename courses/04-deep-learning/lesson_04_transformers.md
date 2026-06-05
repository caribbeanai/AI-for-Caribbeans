# Lesson 4, Transformers, intuition

The Transformer is the model behind modern LLMs. The key idea is attention.

## Attention in one sentence

Each token looks at every other token in the sequence and pulls in information based on how relevant they are.

## Why this beat RNNs

- Parallel training. RNNs process step by step. Transformers process the whole sequence at once.
- Long range memory. Attention reaches across the whole sequence without a fading state.
- Scaling laws. Larger Transformers trained on more data keep getting better, longer than expected.

## Encoder, decoder, both

- Encoder only: good for classification and embeddings, e.g. BERT.
- Decoder only: good for generation, e.g. GPT, Claude, Llama.
- Encoder-decoder: good for translation and summarisation, e.g. T5.

## What to know without going deep

- Tokens: the model sees subword pieces, not characters or words.
- Context window: how many tokens it can read at once. Modern models handle hundreds of thousands.
- Temperature: randomness at sampling time. 0 is greedy, higher is creative.
- Top-p: sample from the smallest set of tokens whose cumulative probability exceeds p.
