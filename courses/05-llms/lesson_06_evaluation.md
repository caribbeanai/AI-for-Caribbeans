# Lesson 6, Evaluation and safety

You cannot improve what you do not measure.

## Levels of evaluation

1. **Vibes.** Look at 20 outputs. Quick, biased, useful for early iteration.
2. **Pairwise.** Compare two model outputs, pick the better one. Use a rubric.
3. **Automatic metrics.** BLEU, ROUGE, embedding similarity. Cheap, blunt.
4. **LLM as judge.** Another model grades. Calibrate it against humans.
5. **Task specific.** Exact match for structured output, business metrics for end use.

## Build an eval set early

Even 30 hand crafted examples is better than nothing. Tag each with the failure mode you saw last time.

## Safety basics

- Refuse personal data. Detect and redact.
- Stop the model from giving legal, medical, or financial advice without disclaimers.
- Guard against prompt injection. Treat user content as untrusted.
- Log everything. Plan for incident review.

## A short test plan

1. 30 happy path queries.
2. 10 edge cases (typos, mixed language, ambiguous questions).
3. 10 adversarial queries (prompt injection, jailbreak attempts).
4. Per release, run all 50 and diff results.
