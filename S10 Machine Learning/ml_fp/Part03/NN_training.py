import torch
from torch.utils.data import DataLoader

def train(
        dataloader: DataLoader,
        model,
        loss_fn,
        optimizer,
        device,
        print_info: bool = False
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
        training_loss += loss.item()
        correct += (pred.argmax(1) == y).type(torch.float).sum().item()

        if print_info and (batch % 100 == 0):
            loss, current = loss.item(), (batch + 1) * len(X)
            print(f"Completed: {current:>5d}/{size:>5d}    loss: {loss:>7f}")
    training_loss /= num_batches
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
        print_info: bool = False
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
    if print_info:
        print(f"Test Accuracy: {(100*correct):>0.1f} %    Test Avg. loss: {test_loss:>8f}")
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
        print_info: bool = False
    ) -> dict:
    train_result: dict = train(
        train_dataloader,
        model,
        loss_fn,
        optimizer,
        device,
        print_info=print_info
    )
    test_result: dict = test(
        test_dataloader,
        model,
        loss_fn,
        device,
        print_info=print_info
    )
    result: dict = train_result | test_result    # union of dicts, no overwrites happen because no keys overlap
    return result