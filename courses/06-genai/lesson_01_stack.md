# Lesson 1, The GenAI stack today

A practical map of what a small team uses to ship.

## Models

- Frontier LLMs: Claude, GPT, Gemini.
- Open weight LLMs: Llama 3, Mistral, Qwen, Phi.
- Image: Flux, Stable Diffusion XL, DALL-E, Midjourney.
- Voice: ElevenLabs, OpenAI TTS, Coqui XTTS, Whisper for transcription.
- Code: Claude, Codex, Copilot.

## Orchestration

- Direct API calls in Python or TypeScript. Fewer dependencies, fewer surprises.
- LangChain or LlamaIndex if you have many moving parts.
- Vercel AI SDK if you are JavaScript first.

## Storage

- Postgres for everything you can fit in it. Add pgvector for embeddings.
- S3 or R2 for files.
- Redis for caching.

## UI

- Streamlit, fastest path to a working app.
- Next.js, when you need polish and SEO.
- Native iOS or Android, when offline and integration matter.

## Hosting

- Render, Railway, Fly.io for small backends.
- Vercel for Next.js apps.
- A small VPS plus Docker is still fine in 2026.

## Observability

- Log every prompt and response. PII redacted.
- Track latency, cost, error rate per route.
- Tools: Helicone, LangSmith, your own SQL table.
