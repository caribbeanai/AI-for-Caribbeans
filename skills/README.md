# Skills

Reusable Claude Code skills for repeated Caribbean workflows. Each skill is a folder containing a `SKILL.md` that explains when to use it and the steps to follow.

## Available skills

- [csec-tutor](csec-tutor/SKILL.md) Tutor a student on a CSEC topic with practice questions.
- [hurricane-brief](hurricane-brief/SKILL.md) Produce a daily hurricane season brief.
- [caribbean-localise-recipe](caribbean-localise-recipe/SKILL.md) Adapt a recipe to local ingredients.
- [country-fact-fetch](country-fact-fetch/SKILL.md) Look up Caribbean country facts from the included dataset.
- [dialect-translate](dialect-translate/SKILL.md) Translate between Caribbean dialects and Standard English.
- [tourism-review-analyse](tourism-review-analyse/SKILL.md) Score and tag a batch of tourism reviews.

- [coauthor-with-evidence](coauthor-with-evidence/SKILL.md) Revise a draft while keeping claims traceable and author decisions visible.
- [develop-with-checkable-changes](develop-with-checkable-changes/SKILL.md) Scope a software change, check acceptance cases and report actual test evidence.
- [kill-my-startup-evidence-check](kill-my-startup-evidence-check/SKILL.md) Challenge startup assumptions, delivery costs and dependencies before a larger commitment.
- [ai-survival-action-plan](ai-survival-action-plan/SKILL.md) Make a practical personal AI preparedness plan and rehearse a verification step.

## How to install in Claude Code

Place a skill folder inside your project's `.claude/skills/` directory, or under your user `~/.claude/skills/`. Each folder needs a `SKILL.md` at minimum.

For now, treat these as documentation. They become invokable once you copy them into the right place.

## Using the four companion skills

Copy the entire chosen folder, including its supporting Markdown files, diagram source and licence. Start with `input-template.md`; the worked example shows a complete synthetic case. `checks-and-tests.md` describes what to check and supplies proposed behavioural tests. Review the instructions before use and keep confidential information out of tools you have not authorised to receive it.

Without installing a skill, open its `SKILL.md` and supporting files and use them as a manual workflow or provide the relevant text to your assistant. A folder’s presence here does not mean it is installed, that its model behaviour has been tested, or that it has permission to send messages, spend money or deploy changes.

Each new companion folder includes the MIT licence and a provenance-and-limits file. Related books and external links retain their own rights. These four folders do not include third-party course material or a course assessment.
