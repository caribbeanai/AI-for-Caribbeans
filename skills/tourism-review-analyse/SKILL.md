# tourism-review-analyse

Score and tag a batch of tourism reviews. Useful for hotels, tour operators, restaurants.

## When to use

- The user pastes a list of reviews.
- The user uploads a CSV of reviews.

## Steps

1. For each review, determine sentiment (positive, mixed, negative).
2. Tag aspects mentioned: rooms, food, service, location, value, cleanliness.
3. Quote the most actionable sentence per review.
4. Produce a summary table with counts and a short narrative of the top three improvement areas.

## Inputs

- Reviews as a list or CSV.

## Output format

A summary section followed by a per review table.
