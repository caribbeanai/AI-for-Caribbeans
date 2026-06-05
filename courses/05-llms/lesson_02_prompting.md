# Lesson 2, Prompting that works

A good prompt has six parts.

1. **Role.** Who the model is. "You are a senior Trinidadian financial advisor."
2. **Task.** What to do. "Summarise this contract in plain English."
3. **Context.** Background information.
4. **Examples.** Two or three input-output pairs.
5. **Constraints.** Length, tone, format.
6. **Output format.** "Return JSON with keys: summary, risks, recommendation."

## A template you can keep

```
You are [ROLE].

Task: [WHAT TO DO]

Context:
[BACKGROUND]

Examples:
Input: ...
Output: ...

Constraints:
- [TONE]
- [LENGTH]
- [ANYTHING ELSE]

Output as [FORMAT].
```

## Tactics that move quality

- Ask the model to think step by step before answering, for reasoning tasks.
- Ask for several drafts, then pick the best, when quality matters.
- Use delimiters to separate sections. Triple backticks, XML tags.
- For structured output, ask for JSON and validate it.
- Give the model permission to say "I do not know." It will hallucinate less.

## Caribbean specific tip

If you want output in a Caribbean voice, give a real sample of that voice in the prompt. Two paragraphs is usually enough.
