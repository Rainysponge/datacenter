import torch
import numpy as np
import pandas as pd
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import json

from models import MLP_base

# 自定义数据集类
class Peak_dataset(Dataset):
    def __init__(self, train=True, datapath=""):
        self.train = train
        # 
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

# 自定义神经网络模型
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
# 加载训练数据
device = 'cuda: 0'

train_dataset = Peak_dataset(train=True, datapath='')
val_dataset = Peak_dataset(train=False, datapath='')
train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=32, shuffle=True)
print(len(train_dataset))
print(len(val_dataset))
# 初始化模型、损失函数和优化器
model = MLP_base()
model = model
criterion = nn.HuberLoss(delta=1.0)
optimizer = optim.SGD(model.parameters(), lr=0.001)

# 训练模型
num_epochs = 300
for epoch in range(num_epochs):
    loss_sum = []
    model.train()
    for idx, (inputs, labels) in enumerate(train_dataloader):
        inputs, labels = inputs, labels
        labels = labels.float().unsqueeze(1)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        loss_sum.append(loss.item())
        loss.backward()
        optimizer.step()

    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {sum(loss_sum) / len(loss_sum)}')
    model.eval()
    with torch.no_grad():
        loss_sum = []
        for idx, (inputs, labels) in enumerate(val_dataloader):
            inputs, labels = inputs, labels
            labels = labels.float().unsqueeze(1)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss_sum.append( loss.item())
        print(f'val Epoch [{epoch+1}/{num_epochs}], Loss: {sum(loss_sum) / len(loss_sum)}')
        with open("/home/users/HuZhanyi/dataspace1/log_save/CINT2017_rate_peak_model_%s.txt" % str(num_epochs), 'w+') as f:
            f.write('')
        with open("/home/users/HuZhanyi/dataspace1/log_save/CINT2017_rate_peak_model_%s.txt" % str(num_epochs), 'a+') as f:
            f.seek(0, 2)
            f.write(f'val Epoch [{epoch+1}/{num_epochs}], Loss: {sum(loss_sum) / len(loss_sum)}\n')


# 保存模型参数
torch.save(model.state_dict(), './CINT2017_rate_peak_model_%s.pth' % str(num_epochs))
