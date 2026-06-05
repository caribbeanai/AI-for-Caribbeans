# Tutorial 4, Build a small RAG over Caribbean facts

We will retrieve from `datasets/caribbean_country_facts.json` and ground an LLM in it.

## Step 1, load and chunk

Each fact is already a small chunk. Read them:

```python
import json
with open("datasets/caribbean_country_facts.json") as f:
    facts = json.load(f)
chunks = [{"country": c, "text": f"{c}: {fact}"} for c, items in facts.items() for fact in items]
```

## Step 2, embed

For a small dataset, TF IDF is enough. For real work, use sentence-transformers or hosted embeddings.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
matrix = vec.fit_transform([c["text"] for c in chunks])
```

## Step 3, retrieve

```python
from sklearn.metrics.pairwise import cosine_similarity

def retrieve(query, k=3):
    q = vec.transform([query])
    sims = cosine_similarity(q, matrix).ravel()
    top = sims.argsort()[::-1][:k]
    return [chunks[i] for i in top]

print(retrieve("Which Caribbean island is known as Spice Isle?"))
```

## Step 4, ground

```python
from anthropic import Anthropic
client = Anthropic()

def answer(q):
    ctx = "\n".join("- " + c["text"] for c in retrieve(q))
    sys = "Answer only from the context. If absent, say you do not know."
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=sys,
        messages=[{"role": "user", "content": f"Context:\n{ctx}\n\nQuestion: {q}"}],
    )
    return resp.content[0].text

print(answer("Which Caribbean island is the Spice Isle?"))
```

## What you learned

- Chunk, embed, retrieve, ground.
- The whole pattern is fewer than 30 lines.

Full script: `courses/05-llms/rag_caribbean_facts.py`.
