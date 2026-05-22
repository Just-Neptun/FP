import torch
from tqdm import tqdm
from Part01.naive_kNN import classify_from_distances


def kNN_classify_fast(
    input_data: torch.Tensor,
    data: torch.Tensor,
    labels: torch.Tensor,
    k: int = 3,
    *,
    debug: bool = False
) -> torch.Tensor:
    """Classify a list of input vectors according to training data/labels.
    Return a list of classifications according to k-NN of input vectors."""
    input_data = torch.flatten(input_data, 1)
    data = torch.flatten(data, 1)
    distances_tensor = torch.cdist(input_data, data)
    input_nearest_labels = (
        classify_from_distances(distances, labels, k) for distances in distances_tensor
    )
    if debug:
        input_nearest_labels = tqdm(input_nearest_labels)
    return torch.Tensor(list(input_nearest_labels))
