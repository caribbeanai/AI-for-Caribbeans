# Deep Learning: Scenarios

## Scenario 1: Coral reef health from snorkel photos

**Setting:** Belize Barrier Reef and Tobago Cays. Tour operators collect daily photos.

**Question:** Classify each photo as healthy, partially bleached, fully bleached.

**Data path:** start with the `sst_anomaly` dataset for context. Collect your own photos. 600 is enough to start with transfer learning.

**Starter:** `courses/04-deep-learning/reef_health_cnn.py`.

**Decision:** when monthly bleached share crosses 25 percent, alert the marine park manager.

## Scenario 2: Bird call identification in the Sisserou Parrot's range

**Setting:** Dominica rainforest. Researchers want passive acoustic monitoring.

**Question:** Classify a 5 second clip as Sisserou Parrot, Mountain Whistler, Trembler, or other.

**Data path:** record from existing protected areas, label with local ornithologists.

**Starter:** `courses/04-deep-learning/bird_call_audio.py`.

## Scenario 3: Sargassum landfall from satellite imagery

**Setting:** Saint Lucia east coast, Tobago, Punta Cana, Tulum. Sargassum mats are a tourism and ecological issue.

**Question:** Given a 3 day satellite sequence, will tomorrow bring a landing on a given beach?

**Approach:** sequence of images plus weather to a small CNN plus LSTM or a Vision Transformer head.

**Decision:** notify hotels and beach cleanup teams 24 hours ahead.

## Scenario 4: Banana plant disease detection

**Setting:** small farmers in Saint Vincent, Saint Lucia, Dominica.

**Question:** From a phone photo, is this Black Sigatoka, Panama disease, or healthy?

**Approach:** a CNN on a few hundred labelled photos per class. Deploy as a WhatsApp bot. Field workers retrain quarterly.

## Scenario 5: Hurricane track refinement

**Setting:** a regional met office wants to refine global model tracks with their own observations.

**Dataset:** `atlantic_storms` for shape. NOAA HURDAT2 for real training.

**Starter:** `courses/04-deep-learning/hurricane_track_lstm.py`.

## Scenario 6: Cricket commentary speech to text

**Setting:** West Indies cricket commentary often blends standard English with regional voices.

**Question:** Build a transcription pipeline with custom vocabulary (player names, ground names).

**Approach:** fine tune Whisper with regional names list, evaluate on five matches.

**Dataset link:** `cricket_matches_wi` for context.
