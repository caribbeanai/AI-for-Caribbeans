# Lesson 2, Convolutional networks for images

Convolutional Neural Networks scan an image with small filters that learn to detect edges, textures, and shapes. Deeper layers combine these into parts, objects, and scenes.

## Building blocks

- Conv2D, the filter that slides across the image.
- ReLU, non linear activation.
- Pooling, reduces spatial size.
- Batch normalisation, stabilises training.
- Dropout, fights overfitting.
- Fully connected layer at the end for classification.

## A modern shortcut

Use a pretrained backbone like ResNet50, EfficientNet, or ConvNeXt from torchvision. Freeze most layers, replace the final layer with your own, train on your small dataset. This is transfer learning and it usually beats training from scratch.

## Caribbean example

Reef bleaching detection from snorkel photos. Three classes: healthy, partially bleached, fully bleached. With 600 training images and a pretrained backbone, a small team can reach useful accuracy in a weekend.

## Data augmentation

Flip horizontally, rotate, crop, jitter colour. These create new training examples for free. Always apply to training data only.
