# LLMs: Scenarios

## Scenario 1: Diaspora remittance support bot

**User:** a Jamaican aunt in Brooklyn wants to send USD 500 home today.

**Goal:** A WhatsApp bot that answers in English or Patois, explains channels, fees, ETA, and limits, and only escalates to a human for KYC issues.

**Pieces:** prompt template + RAG over the provider's policy doc + tool to call a live rate API.

**Dataset:** `remittance_transactions`, `remitter_diaspora_panel`.

## Scenario 2: CSEC exam tutor

**User:** a Form 4 student in Saint Vincent preparing for English A.

**Goal:** A tutor that explains topics, sources from the CXC syllabus, gives feedback on practice essays.

**Pieces:** retrieval over CXC syllabus PDFs, agent loop with `lookup_topic` and `score_essay` tools.

**Starter:** `courses/05-llms/csec_tutor_agent.py`.

## Scenario 3: Tourist concierge for Saint Lucia

**User:** a first time visitor staying in Soufrière.

**Goal:** A bot that books, advises, translates to and from Kwéyòl, and adjusts to budget.

**Pieces:** prompt template `applications/tourism/itinerary_generator_prompt.md` + tool calls to a real booking API + a fallback to a human concierge.

## Scenario 4: Small claims court explainer

**User:** a Bridgetown resident with a dispute over rent.

**Goal:** Explain the small claims process in plain English with links to local forms.

**Pieces:** RAG over Barbados Magistrates' Court website + a strict disclaimer pattern. Never give legal advice.

## Scenario 5: Hurricane prep household bot

**User:** a household in Nassau two days before a tropical storm.

**Goal:** Daily brief, household checklist, shelter locator, post storm damage reporter.

**Pieces:** `prompt-templates/hurricane_brief.md`, tool integrations with the National Hurricane Center feed, shelter list.

## Scenario 6: Cooperative susu tracker

**User:** a 12 person susu in Castries.

**Goal:** A bot that tracks payments, sends reminders, and confirms payouts each round.

**Pieces:** structured outputs (JSON), simple state in Postgres, WhatsApp Cloud API.

## Common pitfalls in our region

- Token cost. Caribbean place and dialect words can use many tokens. Cache aggressively.
- Latency. Many users are on patchy mobile data. Stream output. Show partial results fast.
- Translation drift. Test dialect generation with native speakers, not just engineers.
- Personal data. Phone numbers, ID numbers, and NIS numbers must be redacted before any prompt.
