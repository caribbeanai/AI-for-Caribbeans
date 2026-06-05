# Tutorial 3, Use an LLM from a Python script

We will call Claude and OpenAI from Python.

## Step 1, install the SDKs

```bash
pip install anthropic openai
```

## Step 2, set a key

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Use a `.env` file in real projects and load it with `python-dotenv`.

## Step 3, the smallest possible call

```python
from anthropic import Anthropic
client = Anthropic()
resp = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    messages=[{"role": "user", "content": "Give me one fact about each English speaking Caribbean country."}],
)
print(resp.content[0].text)
```

## Step 4, add a system prompt

```python
resp = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    system="You are a Caribbean knowledge assistant. Be direct, warm, accurate.",
    messages=[{"role": "user", "content": "Explain Crop Over in three sentences."}],
)
```

## Step 5, structure the output

Ask for JSON. Then validate it.

```python
import json
resp = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    system="Return only valid JSON.",
    messages=[{"role": "user", "content": 'Return {"country": "Barbados", "national_dish": "..."} for cou cou and flying fish.'}],
)
data = json.loads(resp.content[0].text)
print(data["national_dish"])
```

## What you learned

- Make an API call.
- Use a system prompt.
- Get structured output.

Working example: `courses/05-llms/chat_basics.py`.
