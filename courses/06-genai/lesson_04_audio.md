# Lesson 4, Voice and audio

Voice products are underexplored in the Caribbean. Many users prefer voice notes to typed messages.

## Use cases

- A WhatsApp bot that accepts a voice note and replies with a voice note.
- A radio call show analytics tool that transcribes and tags calls.
- A field worker app that records observations in Kreyol and stores searchable text.
- A grandmother story preserver that captures and transcribes elder voices.

## Pieces

- Speech to text. Whisper open source, or hosted ASR with custom vocabulary.
- Translation, if needed.
- Text generation with an LLM.
- Text to speech. Voice cloning where you have consent.

## Tips for Caribbean speech

- Train custom vocabularies with local place names and proper nouns.
- Use a higher beam size on Whisper for accent heavy audio.
- Always run a human review on transcripts before they become public.
- Get explicit consent for voice cloning. Always.
