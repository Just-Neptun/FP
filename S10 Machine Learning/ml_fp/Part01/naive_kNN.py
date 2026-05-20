import torch
from collections import Counter
from itertools import chain
from tqdm import tqdm

def get_most_common_entry(lst: list[int | float]) -> int | float:
    '''Return the entry which is most common in a list.'''
    return Counter(lst).most_common(1)[0][0]    # return [(label, #occurences)][0][0]

def euclidean_distance(input_data: torch.Tensor, data: torch.Tensor) -> torch.Tensor:
    '''Calculate distances for all items in input_data to all items in data.
    Returns a (rank 2) tensor: input elements x data elements'''
    if input_data.shape[1:] != data.shape[1:]:
        raise ValueError(f'''Test data and training data feature shapes/dimensions do not match after first dimension!
                         test ≠ input: {input_data.shape} ≠ {data.shape}''')
    data = data[None,:]
    input_data = input_data[:, None]
    difference = input_data - data
    summation_dims = tuple(range(2, difference.ndim))
    distances = (difference**2).sum(dim=summation_dims).sqrt()
    return distances

def classify_from_distances(distances: torch.Tensor, labels: torch.Tensor, k: int) -> int | float:
    '''Return the most common label of the nearest k training vectors given a 1d list of distances to all training vectors.'''
    labelled_distances = torch.stack([distances, labels], dim=-1)
    labelled_distances = labelled_distances.tolist()
    labelled_distances.sort(key=lambda x: x[0])
    k_nearest_labels = [label for _, label in labelled_distances[:k]]
    return get_most_common_entry(k_nearest_labels)

def kNN_classify(
    input_data: torch.Tensor,
    data: torch.Tensor,
    labels: torch.Tensor,
    k: int = 5,
    *,
    debug: bool=False
) -> torch.Tensor:
    '''Classify a list of input vectors according to training data/labels.
    Return a list of classifications according to k-NN of input vectors.'''
    distances_tensor = euclidean_distance(input_data, data)
    input_nearest_labels = (classify_from_distances(distances, labels, k) for distances in distances_tensor)
    if debug: input_nearest_labels = tqdm(input_nearest_labels)
    return torch.Tensor(list(input_nearest_labels))

def kNN_classify_batched(
        input_data: torch.Tensor,
        data: torch.Tensor,
        labels: torch.Tensor,
        k: int,
        batch_size: int,
        *,
        debug: bool = False
) -> torch.Tensor:
    '''Classify a list of input vectors according to training data/labels.
    Return a list of classifications according to k-NN of input vectors.
    Batched calculations according to batch_size to avoid tensors which are too large.
    Debug information can be enabled.'''
    if not (0 < batch_size <= len(input_data)): raise ValueError(f'batch_size is not int between 0 and input_data length! --> {batch_size}')
    batch_indices = range(0, len(input_data), batch_size)
    # slicing is forgiving, allows lst[0:len(lst)+1] as lst[0:len(lst)], so i+batch_size below is OK.
    # produce flattened list => chain.from_iterable appends all created classification lists of batches together
    classification_iterable = (
        kNN_classify(input_data[i:i+batch_size], data, labels, k, debug=False)
        for i in batch_indices
    )
    if debug:
        print(f'total inputs to analyze: {len(input_data)}')
        print(f'total batches: {len(batch_indices)}')
        classification_iterable = tqdm(classification_iterable)
    classification_labels = torch.Tensor(list(chain.from_iterable(classification_iterable)))
    return classification_labels