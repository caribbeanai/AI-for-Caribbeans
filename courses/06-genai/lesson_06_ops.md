# Lesson 6, Cost, latency, and reliability

The boring parts that decide whether your product survives.

## Cost levers

- Use smaller models where they are good enough. Haiku and Mini class models often suffice.
- Cache prompts. Most providers offer prompt caching with deep discounts.
- Use embeddings for classification before paying for generation.
- Truncate context to what is needed. Trim aggressively.

## Latency levers

- Stream responses. Perceived latency drops by half.
- Pre warm long context with caching.
- Run lightweight first pass model, escalate only when needed.

## Reliability

- Implement timeouts and retries with exponential backoff.
- Fallback model. If your primary fails, route to a backup.
- Set max tokens to protect against runaway outputs.
- Validate structured outputs against a schema. Reject and retry on bad output.

## A small SLA you can promise

- p50 latency under 2 seconds for short prompts.
- p95 latency under 6 seconds.
- 99.5 percent successful response rate.
- Cost per active user per month under $X (set by your pricing).
