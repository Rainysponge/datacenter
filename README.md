# datacenter
ECNU数据中台课程作业

按照正常django的配置方法配置即可
- pip -r request.txt
- 配置好相应的数据库端口和密码
- 将json写道数据库中，我应该给出了相应接口
- 数据模型并没有放在里面，但也有相应的接口，运行即可完成数据转换和训练
- 一些关于django的默认配置调整这里就不做赘述了
- 当一切都没有问题之后，python manage.py runserver!

## 训练
当数据被写入数据库后，通过接口/dataspace/data_create
完成之后通过/dataspace/train_* 来完成SVM和决策树的训练
神经网络的训练代码后续会传上来，模型结构如下,其实自己训练一下也是很快的
```python
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
```
感谢黑马老师提供的数据大屏划分区域的代码

ps: 4k和1080p的前端确实有点映射关系，但是不多
