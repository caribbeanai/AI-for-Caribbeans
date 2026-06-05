# Lesson 3, Retrieval Augmented Generation

LLMs do not know your local data. They were trained on the public web at a point in time. RAG fixes that.

## The pattern

1. Take your documents (PDFs, CSVs, Notion pages, websites).
2. Split them into chunks.
3. Compute an embedding for each chunk and store it in a vector database.
4. When the user asks a question, embed the question and retrieve the closest chunks.
5. Send the question and the retrieved chunks to the LLM as context.

## Tools

- Embeddings: OpenAI embeddings, Cohere, Anthropic via partner providers, or open source sentence-transformers.
- Vector store: pgvector, Chroma, Weaviate, Pinecone, Qdrant, LanceDB.
- Orchestration: LangChain, LlamaIndex, or your own 200 lines of Python.

## Why it matters in our region

- Ground the model in actual island data, laws, statistics, schedules.
- Build a tutor that uses CXC syllabi instead of guesses.
- Build customer support bots over a hotel's actual policies.
- Build a legal helper over Caribbean Community case law.

## Pitfalls

- Bad chunks make bad answers. Keep chunks at 300 to 800 tokens with overlap.
- Old data answered with confidence. Date your documents. Filter at query time.
- Hallucinations on missing data. Tell the model to refuse when no relevant chunks are found.
