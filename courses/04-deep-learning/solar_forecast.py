"""
Scenario: forecast next hour solar irradiance for a residential PV planning study.
Uses datasets/solar_irradiance.csv. Tiny LSTM as a teaching example.

Author: Adrian Dunkley
"""

from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parents[2] / "datasets" / "solar_irradiance.csv"

try:
    import torch
    from torch import nn
except ImportError:
    raise SystemExit("Install torch to run this script.")


class TinyLSTM(nn.Module):
    def __init__(self, input_size=3, hidden=32):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden, batch_first=True)
        self.head = nn.Linear(hidden, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.head(out[:, -1, :]).squeeze(-1)


def windows(arr, lookback=6):
    X, y = [], []
    for i in range(lookback, len(arr)):
        X.append(arr[i - lookback:i])
        y.append(arr[i, 0])
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)


def main():
    df = pd.read_csv(DATA)
    site = df[df["site"] == "Kingston"].sort_values("timestamp").reset_index(drop=True)
    arr = site[["ghi_w_m2", "temperature_c", "cloud_cover_pct"]].to_numpy(dtype=np.float32)
    X, y = windows(arr)
    split = int(len(X) * 0.8)
    Xtr, Xte = torch.tensor(X[:split]), torch.tensor(X[split:])
    ytr, yte = torch.tensor(y[:split]), torch.tensor(y[split:])

    model = TinyLSTM()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.MSELoss()
    for epoch in range(20):
        opt.zero_grad()
        loss = loss_fn(model(Xtr), ytr)
        loss.backward()
        opt.step()
    mae = (model(Xte).detach().numpy() - yte.numpy()).__abs__().mean()
    print(f"Test MAE: {mae:.1f} W/m^2")


if __name__ == "__main__":
    main()
