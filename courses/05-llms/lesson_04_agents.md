# Lesson 4, Tools, agents, and orchestration

A tool is a function the model can call. An agent is an LLM that uses tools in a loop.

## Tool calling

You expose Python functions like `get_weather(city)`, `lookup_exchange_rate(base, quote, date)`, `search_csec_syllabus(subject, topic)`. The LLM decides when to call them, parses the result, and continues.

## Agent loops

1. User asks.
2. Model reasons and proposes a tool call.
3. Tool runs.
4. Result returns to the model.
5. Model decides: another tool, or final answer.

## What makes agents useful

- Real time data: weather, exchange rates, news.
- Computation the model is bad at: maths, complex parsing.
- Database access: search a hotel inventory or a tax code.
- Side effects: send an email, book a slot.

## Caution

- Give the agent the smallest set of tools it needs.
- Log every tool call.
- Limit destructive tools behind explicit confirmation.
- Set a maximum step count.

## Caribbean agent ideas

- A travel concierge that books inter island flights and ferries.
- A small business assistant that drafts WhatsApp replies and schedules them.
- A study agent that pulls past CXC papers and quizzes a student.
