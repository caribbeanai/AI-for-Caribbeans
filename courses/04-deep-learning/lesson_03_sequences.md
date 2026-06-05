# Lesson 3, Sequence models and RNNs

Some data has order: time series, text, audio. Sequence models read it in order.

## Recurrent Neural Networks

The network processes one step at a time, keeping a hidden state that carries memory.

## LSTM and GRU

Variants designed to remember longer. They were the workhorses of NLP and forecasting through the 2010s.

## Today

Most sequence tasks are now done with Transformers. RNNs remain useful for small embedded devices, very long sequences with linear attention variants, and as a teaching baseline.

## Caribbean example, hurricane tracking

Given a sequence of positions and intensities for the past 24 hours, predict where a hurricane will be in 6, 12, 24, and 48 hours. NOAA has decades of training data freely available.
