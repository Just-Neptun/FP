import torch

def get_device():
    '''
    Use torch to find the best device on the hardware to use.
    Priority order: 'cuda', 'mps, 'cpu'
    '''
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")