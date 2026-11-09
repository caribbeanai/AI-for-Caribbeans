# Teaching example

## Request
Teach an insurance administrator to use AI to summarise a supplied policy clause. No real customer data. Include a prompt and a practical learning check.

## Response checks
Supply a short teaching clause or ask for the clause, keep policy decisions human-owned, require source-aligned wording, distinguish a teaching rubric from validated certification.


## Completed exercise
Teaching clause: “For this exercise, a claim requires a completed form and a repair estimate. Submit both within 30 calendar days of the incident. This clause does not state whether late claims are accepted.”
Task: draft a plain-language checklist. A qualified reviewer retains coverage and acceptance decisions.
Copy-ready prompt: “Use only the clause below. List the required documents and deadline in plain language. Quote the words supporting each item. Mark questions the clause does not answer. Do not decide coverage or accept a late claim. Output: checklist, supporting words, questions for the reviewer. Clause: [paste approved clause].”
Expected checklist: completed form; repair estimate; submit both within 30 calendar days of the incident. Late-claim acceptance is unknown from the clause.
Neglected D: a draft says late claims are automatically rejected. Discernment check: locate the supporting sentence. None exists. Correction: remove that claim and refer the question to the reviewer.
Task-specific scoring: Delegation 2 requires reserving coverage/acceptance decisions for a person; 1 mentions review without its scope; 0 lets AI decide. Description 2 supplies the clause, format and limits; 1 misses one; 0 gives only “summarise”. Discernment 2 checks each item against the clause and detects the invented rejection; 1 checks only completeness; 0 accepts the answer. Diligence 2 records the clause version, reviewer and data restrictions; 1 records some; 0 records none.
The prepared prompt is not evidence of the learner's score. Save the learner's baseline response and repeat on a comparable clause with different required documents. Score the actual responses, not the passage of time.
