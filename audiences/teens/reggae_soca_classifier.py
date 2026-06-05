"""
Reggae versus Soca classifier from lyrics keywords.
A tiny example to show how text features become predictions.
This is not a serious model, it teaches the idea.

Author: Adrian Dunkley
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

lyrics = [
    "one love one heart let's get together and feel alright",
    "rasta vibration jah guide and protect",
    "redemption song freedom from mental slavery",
    "babylon system is the vampire",
    "wave your flag we jamming on the road",
    "palance palance everybody jump and wave",
    "soca jumbie wining down the road in trinidad",
    "fete all night carnival monday tuesday",
    "bumper roll she waist deep in the bacchanal",
    "iron from monday morning the rhythm hot",
]
labels = ["reggae", "reggae", "reggae", "reggae",
          "soca", "soca", "soca", "soca", "soca", "soca"]

pipeline = Pipeline([
    ("vec", CountVectorizer()),
    ("clf", LogisticRegression(max_iter=1000)),
])
pipeline.fit(lyrics, labels)

tests = [
    "jah love guide my path through babylon streets",
    "everybody wave a flag carnival is here",
]
for t in tests:
    print(f"{t!r} -> {pipeline.predict([t])[0]}")
