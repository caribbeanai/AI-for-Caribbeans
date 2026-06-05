# country-fact-fetch

Look up authoritative facts about Caribbean countries using the bundled dataset.

## When to use

- The user asks a factual question about a Caribbean country.
- The user needs a quick reference card for a presentation.

## Steps

1. Read `datasets/caribbean_country_facts.json`.
2. Match the country name (handle common variations like "DR", "T&T").
3. Return the facts list verbatim, then add a one paragraph summary in plain English.
4. If the user asks a fact not in the dataset, say so and offer to look it up via a web search if available.

## Inputs

- Country name

## Output format

Bulleted facts, then a one paragraph summary.
