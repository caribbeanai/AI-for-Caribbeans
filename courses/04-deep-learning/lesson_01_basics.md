# Lesson 1, Neural network basics

A neural network is layers of small functions stacked. Each layer multiplies inputs by weights, adds a bias, and applies a non-linear activation. Stacking lets the network represent complex relationships.

## The smallest useful unit

```
y = activation(W * x + b)
```

## Common activations

- ReLU. Default for hidden layers.
- Sigmoid. Use for binary outputs.
- Softmax. Use for multi-class outputs.
- Tanh. Used in some sequence models.

## Training

- Forward pass, compute predictions.
- Loss, compare predictions to truth.
- Backpropagation, compute gradients of the loss with respect to weights.
- Optimiser, update weights. Adam is a safe default.

## When to reach for deep learning

- You have lots of unstructured data (images, audio, text).
- Tabular alternatives have plateaued.
- You have GPUs or a budget for them.

## When not to

- Small tabular dataset. Use gradient boosting.
- Need interpretability. Trees or linear models are clearer.
- Tight latency or device constraints with no model optimisation effort.
