import torch
import numpy as np
import pandas as pd
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import json

datapath = ""

class Base_dataset(Dataset):
    def __init__(self, train=True, datapath=""):
        self.train = train
        df = pd.read_json(datapath)
        condition = df['peak'] > 0
        df = df[condition]

        X = df[['L1_I', 'L1_D', 'L2', 'L3', 'hz', "Base_Pointers", 'Peak_Pointers', 'Memory', 'cores', 'Nominal', 'peak']]

        idxs = np.random.permutation(len(X))
        train_idxs = idxs[500:]
        test_idxs = idxs[:500]
        train = np.array(X)[train_idxs]
        test = np.array(X)[test_idxs]

        


        train_data = train[:, :10]
        train_lab = train[:, 10]

        test_data = test[:, :10]
        test_lab = test[:, 10]
        if self.train:
            self.data = torch.from_numpy(train_data).float()
            self.target = torch.tensor(train_lab).float()
        else:
            self.data = torch.from_numpy(test_data).float()
            self.target = torch.tensor(test_lab).float()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        data, target = self.data[idx], int(self.target[idx])
        return data, target


class MLP_base(nn.Module):
    def __init__(self):
        super(MLP_base, self).__init__()
        self.fc1 = nn.Linear(10, 256)
        self.fc2 = nn.Linear(256, 256)
        self.fc3 = nn.Linear(256, 256)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        
        self.fc4 = nn.Linear(256, 1)
        
        

    def forward(self, x):
        x = self.sigmoid(self.fc1(x))
        x = self.sigmoid(self.fc2(x))
        x = self.sigmoid(self.fc3(x))
        x = self.fc4(x)

        return x

    # /home/users/HuZhanyi/dataspace/CFP2017_rate.json


if __name__ == '__main__':
    model = MLP_base()
    model.load_state_dict(torch.load(model_path))
    model.eval()

    val_dataset = Base_dataset(train=False, datapath=datapath)

    val_dataloader = DataLoader(val_dataset, batch_size=30, shuffle=True)

    # for idx, (inputs, targets) in enumerate(val_dataloader):
    #     # print(inputs, targets)
    #     print(targets)
    #     output = model(inputs)
    #     print(output)
    #     break
    df = pd.read_json(datapath)
    X = df[['L1_I', 'L1_D', 'L2', 'L3', 'hz', "Base_Pointers", 'Peak_Pointers', 'Memory', 'cores', 'Nominal', 'peak']]
    a = np.array(X[:1])[0][:10]
    model = model.double()
    a = torch.tensor(a, dtype=torch.double)
    print(model(a))
