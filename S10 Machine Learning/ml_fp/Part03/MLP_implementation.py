import torch
from torch import nn

from typing import Literal

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(3*64*64, 512),    # RGB 64 x 64 images (from GalaxyMNIST datset)
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 4),    # 4 classes (types of galaxies in dataset)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

    # def classify(self, input):
    #     logits = self(input)
    #     pred_probab = nn.Softmax(dim=1)(logits)
    #     y_pred = pred_probab.argmax(1)
    #     return y_pred

# =====-----=====-----=====-----=====

def train(
        dataloader: torch.utils.data.DataLoader,
        model,
        loss_fn,
        optimizer,
        device
    ) -> dict:
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.train()
    training_loss, correct = 0, 0
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        # Compute error in output (the model prediction)
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        # Accumulate loss and corrects
        training_loss += loss
        correct += (pred.argmax(1) == y).type(torch.float).sum().item()

        if batch % 100 == 0:
            loss, current = loss.item(), (batch + 1) * len(X)
            print(f"Completed: {current:>5d}/{size:>5d}    loss: {loss:>7f}")
    training_loss /= num_batches
    correct /= size
    return {
        'training_avg_loss': training_loss,
        'training_accuracy': correct
    }

def test(
        dataloader: torch.utils.data.DataLoader,
        model,
        loss_fn,
        device
    ) -> dict:
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \nAccuracy: {(100*correct):>0.1f} %    Avg. loss: {test_loss:>8f}")
    return {
        'test_avg_loss': test_loss,
        'test_accuracy': correct
    }