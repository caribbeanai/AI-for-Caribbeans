# Lesson 3, Feature engineering for Caribbean data

The model is only as good as the features you feed it. Here are patterns we see again and again in regional data.

## Time features

- Hurricane season indicator, June 1 to November 30.
- Tourism high season versus low season. Different by island.
- School term versus holiday.
- Carnival, Crop Over, Junkanoo, day of, week of.

## Geographic features

- Parish or district code.
- Distance to coastline.
- Elevation. Important for both rainfall and damage modelling.
- Cruise port or not.

## Economic features

- Exchange rate at the date of the transaction.
- Remittance volume month over month change.
- Local CPI, where available.

## Categorical handling

- One hot encode small categoricals (under 10 levels).
- Use target encoding for high cardinality categoricals, with care.

## Text features

- Word counts for short text.
- TF IDF for medium text.
- Sentence embeddings for longer text. Use a multilingual model so it handles English, Spanish, French, Dutch, and Kreyol.

## Image features

- Resize to a consistent shape.
- Normalise pixel values.
- Use a pretrained backbone (ResNet, EfficientNet) and add your own head.

## Practical tip

Write feature creation as functions, not inline. You will need to apply the same transforms at inference time. A common bug is training one way and inferring another.
