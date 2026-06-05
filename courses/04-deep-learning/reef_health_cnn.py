"""
Scaffold for a coral reef health image classifier.
You provide images organised as:

  data/reef/train/healthy/
  data/reef/train/partial/
  data/reef/train/bleached/
  data/reef/val/...

This file shows the structure of training with a pretrained backbone.
Install requirements first. GPU recommended but not required for small data.

Author: Adrian Dunkley
"""

import os
from pathlib import Path

try:
    import torch
    from torch import nn, optim
    from torch.utils.data import DataLoader
    from torchvision import datasets, transforms, models
except ImportError:
    raise SystemExit("Install torch and torchvision first. See requirements.txt")

DATA_DIR = Path(os.environ.get("REEF_DATA_DIR", "data/reef"))


def build_loaders(image_size=224, batch_size=32):
    train_tf = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(0.2, 0.2, 0.2),
        transforms.ToTensor(),
    ])
    val_tf = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
    ])
    train_ds = datasets.ImageFolder(DATA_DIR / "train", transform=train_tf)
    val_ds = datasets.ImageFolder(DATA_DIR / "val", transform=val_tf)
    return (
        DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=2),
        DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=2),
        train_ds.classes,
    )


def build_model(num_classes):
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    for p in model.parameters():
        p.requires_grad = False
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model


def train(epochs=5, lr=1e-3):
    if not DATA_DIR.exists():
        print(f"Place your data under {DATA_DIR}. This is a scaffold.")
        return
    train_loader, val_loader, classes = build_loaders()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = build_model(len(classes)).to(device)
    opt = optim.Adam(model.fc.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        model.train()
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            opt.zero_grad()
            loss = loss_fn(model(x), y)
            loss.backward()
            opt.step()
        model.eval()
        correct = total = 0
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)
                preds = model(x).argmax(1)
                correct += (preds == y).sum().item()
                total += y.size(0)
        print(f"Epoch {epoch + 1} val accuracy: {correct / total:.3f}")


if __name__ == "__main__":
    train()
