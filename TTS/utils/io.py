import torch
from TTS.tts.configs.xtts_config import XttsConfig

# Allowlist the XttsConfig class
torch.serialization.add_safe_globals([XttsConfig])

def load_fsspec(f, map_location=None, **kwargs):
    return torch.load(f, map_location=map_location, weights_only=False, **kwargs)
