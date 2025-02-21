import torch

def load_fsspec(f, map_location=None, **kwargs):
    return torch.load(f, map_location=map_location, weights_only=False, **kwargs)
