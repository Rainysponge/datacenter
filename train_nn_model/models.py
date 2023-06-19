import torch
import numpy as np
import pandas as pd
import torch.nn as nn
import torch.optim as optim

class MLP_base(nn.Module):
    def __init__(self):
        super(MLP_base, self).__init__()
        self.fc1 = nn.Linear(10, 256)
        self.fc2 = nn.Linear(256, 256)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        self.fc3 = nn.Linear(256, 1)
        
        

    def forward(self, x):
        x = self.sigmoid(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)

        return x

