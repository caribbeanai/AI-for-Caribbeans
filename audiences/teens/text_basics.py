"""
Text basics. Count words, find the most common word, and clean dialect text.
Sample text uses Caribbean voices.

Author: Adrian Dunkley
"""

from collections import Counter
import re

sample = """
Wah gwaan Kingston, di sun a beat down hard today.
Trini people, allyuh come for de bake an shark in Maracas.
In Bridgetown we lime by the gap and eat cou cou.
Saint Lucia mountains tall like cathedral, the Pitons watching.
"""


def clean(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    return text.split()


words = clean(sample)
counts = Counter(words)
print("Most common five words:", counts.most_common(5))
print("Total words:", len(words))
print("Unique words:", len(set(words)))
