# Course 05, Large Language Models

LLMs are general purpose text engines. This course teaches you to use them well, ground them in your own data, and where useful, fine tune them.

## Lessons

1. [Anatomy of an LLM](lesson_01_anatomy.md)
2. [Prompting that works](lesson_02_prompting.md)
3. [Retrieval Augmented Generation, RAG](lesson_03_rag.md)
4. [Tools, agents, and orchestration](lesson_04_agents.md)
5. [Fine tuning and LoRA](lesson_05_fine_tuning.md)
6. [Evaluation and safety](lesson_06_evaluation.md)
7. [Dialect, code switching, and Caribbean language](lesson_07_dialect.md)

## Scenarios

See [scenarios.md](scenarios.md) for six LLM scenarios spanning remittance support, CSEC tutoring, tourist concierge, court explainer, hurricane prep, and susu tracking.

## Datasets

Full index in [../../datasets/CATALOG.md](../../datasets/CATALOG.md).

## Code

- [chat_basics.py](chat_basics.py), a minimal Claude and OpenAI client.
- [rag_caribbean_facts.py](rag_caribbean_facts.py), a tiny RAG over Caribbean country facts.
- [patois_translator.py](patois_translator.py), patois to formal English helper.
- [csec_tutor_agent.py](csec_tutor_agent.py), a tutor with a small tool set.
- [diaspora_remittance_bot.py](diaspora_remittance_bot.py), a grounded support bot skeleton.

## Capstone

Build a chatbot that helps a specific Caribbean audience. A WhatsApp like UI is enough. Ground it in real local facts. Test it with five real users from your target group.
