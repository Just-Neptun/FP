import torch
from torch.utils.data import DataLoader
import pandas as pd

from tqdm.notebook import tqdm

from collections.abc import Sized
from typing import cast

def get_dataloader_len(
        dataloader: DataLoader
    ) -> int:
    '''
    Return number of samples in the dataloader/dataset.
    Uses typechecking cast() to appease typechecker (no runtime difference).
    '''
    return len(cast(Sized, dataloader.dataset))


def train(
        dataloader: DataLoader,
        model,
        loss_fn,
        optimizer,
        device
    ) -> dict:
    size = get_dataloader_len(dataloader)
    model.train()
    training_loss, correct = 0, 0
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)
        # Zero the accumulated gradients of parameters (set tensor to None for better performance)
        optimizer.zero_grad(set_to_none=True)
        # Run model in training mode and compute error in output (the model prediction)
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        loss.backward()
        optimizer.step()

        # Accumulate loss and number of correct predictions
        training_loss += loss.item() * len(X)
        correct += (pred.argmax(1) == y).type(torch.float).sum().item()

    # calculate average loss and accuracy over whole training step
    training_loss /= size
    correct /= size
    return {
        'training_avg_loss': training_loss,
        'training_accuracy': correct
    }

def test(
        dataloader: DataLoader,
        model,
        loss_fn,
        device
    ) -> dict:
    size = get_dataloader_len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item() * len(X)
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= size
    correct /= size
    return {
        'test_avg_loss': test_loss,
        'test_accuracy': correct
    }


def training_step(
        model: torch.nn.Module,
        train_dataloader: DataLoader,
        test_dataloader: DataLoader,
        loss_fn,
        optimizer,
        device
    ) -> dict:
    train_result: dict = train(
        train_dataloader,
        model,
        loss_fn,
        optimizer,
        device
    )
    test_result: dict = test(
        test_dataloader,
        model,
        loss_fn,
        device
    )
    result: dict = train_result | test_result    # union of dicts, no overwrites happen because no keys overlap
    return result


def training_loop(
        model: torch.nn.Module,
        train_dataloader,
        test_dataloader,
        loss_fn,
        optimizer,
        epochs: int,
        DEVICE
    ) -> list[dict]:
    result: list[dict] = []
    for t in tqdm(range(epochs)):
        res: dict = training_step(
            model,
            train_dataloader,
            test_dataloader,
            loss_fn,
            optimizer,
            DEVICE,
        )
        result.append({'epoch': t} | res)    # union of dicts, no overwrites happen because no keys overlap
    return result

def loss_and_accuracy_plot(axes, df: pd.DataFrame) -> None:
    ax1, ax2 = axes[0], axes[1]

    ax1.plot(df['epoch'], df['training_avg_loss'], label='Training', marker='.')
    ax1.plot(df['epoch'], df['test_avg_loss'], label='Testing', marker='.')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Average Loss')
    ax1.set_title('Loss During Training and Testing')
    ax1.legend()

    ax2.plot(df['epoch'], df['training_accuracy'], label='Training', marker='.')
    ax2.plot(df['epoch'], df['test_accuracy'], label='Testing', marker='.')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.set_title('Accuracy During Training and Testing')
    ax2.legend()