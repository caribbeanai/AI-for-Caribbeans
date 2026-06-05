"""
Scaffold for classifying Caribbean bird calls.
The Doctor Bird (Jamaica), the Magnificent Frigatebird (Barbuda),
the Sisserou Parrot (Dominica), the Scarlet Ibis (Trinidad).

You provide WAV or MP3 files in folders by species. We convert to mel
spectrograms and train a small CNN on top of them.

Author: Adrian Dunkley
"""

from pathlib import Path
import os

print("This is a scaffold. To run end to end, install torchaudio and provide")
print("audio files under data/birds/<species>/*.wav. See lesson 02 for the")
print("transfer learning pattern. The pipeline:")
print("  1) Load audio with torchaudio.")
print("  2) Convert to mel spectrogram (n_mels=64, hop_length=512).")
print("  3) Treat as a single channel image and feed to a small CNN.")
print("  4) Or fine tune a model from Hugging Face like wav2vec2.")
