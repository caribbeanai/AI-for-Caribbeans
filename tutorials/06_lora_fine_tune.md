# Tutorial 6, Fine tune an open weight model with LoRA

A practical recipe. Skip this if prompting plus RAG works for your problem.

## What you need

- A GPU. Free options: Google Colab, Kaggle, Modal credits, RunPod.
- A dataset in chat format, 500 to 5000 examples.
- Hugging Face account.

## Dataset format

```json
{"messages": [
  {"role": "system", "content": "You are a Saint Lucia tourism concierge."},
  {"role": "user", "content": "What can I do in Soufrière for a day?"},
  {"role": "assistant", "content": "..."}
]}
```

Save as JSONL.

## Pick a base model

Llama 3 8B, Mistral 7B, or Qwen 2 7B are practical starting points.

## Train with PEFT

```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer

base = "meta-llama/Meta-Llama-3-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(base)
model = AutoModelForCausalLM.from_pretrained(base, load_in_8bit=True, device_map="auto")

lora = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"], lora_dropout=0.05, task_type="CAUSAL_LM")
model = get_peft_model(model, lora)

# Dataset prep and Trainer setup omitted; see Hugging Face docs.
```

## Evaluate

Hold out 100 examples. Compare base versus fine tuned on those. Use exact match where applicable, an LLM judge for free form.

## Deploy

Push the adapter to Hugging Face. Load it at inference time on top of the base model. Or merge and convert to GGUF for local CPU inference.

## When to stop

If your eval is not improving across two training runs with different hyperparameters, the problem is probably your data quality, not the model. Improve the data, then try again.
