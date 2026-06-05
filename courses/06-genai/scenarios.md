# GenAI: Scenarios

Six product shaped scenarios. For each, the goal is a small thing real people will use, not a science project.

## Scenario 1: "Granny's Stories", an elder story preserver

**Customer:** Caribbean families who want to capture grandparents' stories before they are lost.

**MVP:** record audio on the phone, transcribe with Whisper, clean up with an LLM, produce a printable PDF and a shareable audio version.

**Why it works:** value is real, price tolerance is high (USD 49 setup, USD 9 per month), and one click sharing fits family WhatsApp culture.

## Scenario 2: "Vibe Plates", a recipe localiser

**Customer:** Caribbean home cooks who follow global YouTube recipes and end up missing ingredients.

**MVP:** paste a recipe URL, get a localised version using ingredients available in your country, with a shopping list and total cost.

**Dataset link:** `market_prices_weekly` for current price estimates.

## Scenario 3: "Reply Quick", a hotel review responder

**Customer:** small hotels with 5 to 30 rooms.

**MVP:** paste a review URL, get three reply drafts in the hotel's voice, post the chosen one back.

**Dataset link:** `tourism_reviews` for training prompts and demos.

## Scenario 4: "Mas Mind", a Carnival planner

**Customer:** first time mas players from the diaspora.

**MVP:** budget aware schedule across Panorama, Jouvert, Monday Mas, Tuesday Mas, with band suggestions, packing list, and a dialect crash course.

**Dataset link:** `carnival_attendance` to time recommendations.

## Scenario 5: "Sun Sizer", a residential PV sizing tool

**Customer:** Caribbean homeowners thinking about solar.

**MVP:** enter address, monthly bill, and roof orientation. Get a recommended panel count, expected payback period, and a vetted installer list.

**Dataset link:** `solar_irradiance` for site specific estimates.

## Scenario 6: "Class Clip", a teacher's lesson media maker

**Customer:** primary school teachers across the OECS.

**MVP:** type a lesson topic, get a one minute illustrated video with local context, ready to share over WhatsApp.

**Pieces:** image generation, text to speech, simple video assembly.

## Ship checklist

- One target customer, named.
- One offer, one price, one currency by default.
- Payment from day one (Stripe with trial).
- A landing page with a 2 minute Loom demo.
- 30 personal outreach DMs in the first week.
- A test plan written before launch.

## Cost discipline

- Use Haiku, Mini, or open weight first. Reach for the flagship only when needed.
- Cache repeated prompts.
- Stream output so perceived latency drops by half.
- Set max tokens to limit runaway costs.
