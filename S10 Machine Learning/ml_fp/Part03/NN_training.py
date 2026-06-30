import torch
from torch.utils.data import DataLoader

from tqdm.notebook import tqdm

from collections.abc import Sized
from typing import cast, Callable

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
        device,
        print_info: bool = False,
        print_function: Callable = print
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

        if print_info and (batch != 0) and (batch % 50 == 0):
            loss, current = loss.item(), (batch + 1) * len(X)
            print_function(f"Completed: {current:>5d}/{size:>5d}    loss: {loss:>7f}")
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
        device,
        print_info: bool = False,
        print_function: Callable = print
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
    if print_info:
        print_function(f"Test Accuracy: {(100*correct):>0.1f} %    Test Avg. loss: {test_loss:>8f}")
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
        device,
        print_info: bool = False,
        print_function: Callable = print
    ) -> dict:
    train_result: dict = train(
        train_dataloader,
        model,
        loss_fn,
        optimizer,
        device,
        print_info=print_info,
        print_function=print_function
    )
    test_result: dict = test(
        test_dataloader,
        model,
        loss_fn,
        device,
        print_info=print_info,
        print_function=print_function
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
    print_function = tqdm.write    # choose instead of print for compatibility with tqdm progress bar
    result: list[dict] = []
    for t in tqdm(range(epochs)):
        print_info = True if (t % 5 == 0 or t == epochs - 1) else False
        if print_info: print_function(f"---------- Epoch {t} ----------")
        res: dict = training_step(
            model,
            train_dataloader,
            test_dataloader,
            loss_fn,
            optimizer,
            DEVICE,
            print_info,
            print_function=print_function
        )
        result.append({'epoch': t} | res)    # union of dicts, no overwrites happen because no keys overlap
    print_function("Done!")
    return result