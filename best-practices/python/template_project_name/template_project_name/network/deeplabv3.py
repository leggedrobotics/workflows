from typing import List

import torch
from torch import nn
import torch.nn.functional as F

class DeepLabV3(nn.Module):
    def __init__(self, cfg_model):
        super().__init__()
        # Using a ready model
        # Alternative define here your layers and network architecture
        self.model = torch.hub.load("pytorch/vision:v0.10.0", cfg_model["type"], pretrained=False)

    def forward(self, data):
        return self.model(data)
