# Lesson 5, Fine tuning and LoRA

Most teams do not need to fine tune. Prompting plus RAG covers 80 percent of use cases. When you do need it, use LoRA.

## When to fine tune

- The style is highly specific and prompting cannot get there.
- You need consistent structured output and tools alone are not enough.
- You want a smaller open weight model to behave like a larger closed model on your domain.
- Privacy and on premise constraints rule out hosted models.

## LoRA in one paragraph

Low Rank Adaptation. Freeze the base model. Insert small trainable matrices into key layers. Train only those. You change 0.1 percent of parameters and get most of the benefit at a fraction of the compute.

## Practical recipe

1. Pick a base. Llama 3 8B or 70B, Mistral 7B, or a Phi family model.
2. Collect 500 to 5000 high quality examples in the target format.
3. Use Hugging Face PEFT and transformers.
4. Train on a single GPU for hours, not days.
5. Evaluate on a held out set with the same metric you care about.

## Caribbean specific note

Open weight models are weak on Kreyol, Papiamento, and Sranan Tongo. A LoRA over a few thousand pairs can lift quality meaningfully. Be careful about data licensing for dialect corpora.
