"""
Scaffold for forecasting a hurricane's next position from a short track history.
Toy synthetic data, illustrates the pipeline.

Author: Adrian Dunkley
"""

import numpy as np

try:
    import torch
    from torch import nn
except ImportError:
    raise SystemExit("Install torch to run this script.")


def synth_track(n_storms=200, seq_len=8, rng=None):
    rng = rng or np.random.default_rng(42)
    X, y = [], []
    for _ in range(n_storms):
        lat = rng.uniform(10, 20)
        lon = rng.uniform(-80, -55)
        dlat = rng.uniform(0.1, 0.6)
        dlon = rng.uniform(-1.0, -0.4)
        track = []
        for step in range(seq_len + 1):
            track.append([lat + dlat * step + rng.normal(0, 0.05),
                          lon + dlon * step + rng.normal(0, 0.05)])
        track = np.array(track)
        X.append(track[:-1])
        y.append(track[-1])
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)


class TrackLSTM(nn.Module):
    def __init__(self, hidden=64):
        super().__init__()
        self.lstm = nn.LSTM(2, hidden, batch_first=True)
        self.head = nn.Linear(hidden, 2)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.head(out[:, -1, :])


def main():
    X, y = synth_track()
    X = torch.tensor(X)
    y = torch.tensor(y)
    model = TrackLSTM()
    opt = torch.optim.Adam(model.parameters(), lr=1e-2)
    loss_fn = nn.MSELoss()
    for epoch in range(50):
        opt.zero_grad()
        loss = loss_fn(model(X), y)
        loss.backward()
        opt.step()
        if (epoch + 1) % 10 == 0:
            print(f"epoch {epoch + 1} loss {loss.item():.4f}")


if __name__ == "__main__":
    main()
