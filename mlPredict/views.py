import torch
import numpy as np
import torch.nn as nn
import json
import joblib
import pandas as pd
from django.db.models import Q
from sklearn.preprocessing import MinMaxScaler
from django.http import JsonResponse
from django.shortcuts import render
from utils.decorators import login_required
from dataspace.models import Benchmark, CFP2017_ratediv_result, SPECrate2017_ratediv_fp_score, \
    SPECrate2017_ratediv_int_score, \
    CINT2017_ratediv_result, SPECrate2017_speeddiv_fp_score, CFP2017_speeddiv_result, SPECrate2017_speeddiv_int_score, \
    CINT2017_speeddiv_result, CFP2017_ratediv, CFP2017_speeddiv, CINT2017_ratediv, CINT2017_speeddiv, \
    CINT2017_speeddiv_hard_soft, CFP2017_speeddiv_hard_soft, CINT2017_ratediv_hard_soft, CFP2017_ratediv_hard_soft, OS
from .os_dict import os_dict

from .forms import MLFrom

# Create your views here.

hs_list = [None, CFP2017_ratediv_hard_soft, CFP2017_speeddiv_hard_soft, CINT2017_ratediv_hard_soft,
           CINT2017_speeddiv_hard_soft]

model_list = [
    None, "svm_regression_model", 'DecisionTreeRegressor'
]

score_list = {

    1: SPECrate2017_ratediv_fp_score,
    2: SPECrate2017_speeddiv_fp_score,
    3: SPECrate2017_ratediv_int_score,
    4: SPECrate2017_speeddiv_int_score

}

MLP_list = {
    1: [
        "raw_data/data/SKL/NNModel/CFP2017_rate_base_model_300.pth",
        'raw_data/data/SKL/NNModel/CFP2017_rate_peak_model_1000.pth'
    ],
    2: [
        "raw_data/data/SKL/NNModel/CFP2017_speed_base_model_500.pth",
        "raw_data/data/SKL/NNModel/CFP2017_speed_peak_model_1000.pth"
    ],
    3: [
        "raw_data/data/SKL/NNModel/CINT2017_rate_base_model_500.pth",
        "raw_data/data/SKL/NNModel/CINT2017_rate_peak_model_1000.pth"
    ],
    4: ["raw_data/data/SKL/NNModel/CINT2017_speed_base_model_500.pth"]
}


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


@login_required
def predict_SVM(request, task_number=None, model_number=None):
    summary_name_list = {

        1: 'CFP2017_rate',
        2: 'CFP2017_speed',
        3: 'CINT2017_rate',
        4: 'CINT2017_speed'

    }
    if model_number == 1:
        model_name = 'SVM'
    else:
        model_name = 'DecisionTree'
    context = {'summary_name_list': summary_name_list, 'massage': '登陆成功', 'model_name': model_name,
               'task_number': task_number, 'model_number': model_number, 'task_name': summary_name_list[task_number]}
    if request.method == 'POST':
        if model_number in [1, 2]:
            model_ = model_list[model_number]
        ml_form = MLFrom(request.POST)
        input_dict = {}
        if ml_form.is_valid():

            # input_dict['cores'] = ml_form.clean_cores()
            input_dict['L1_I'] = ml_form.clean_L1_I()
            input_dict['L1_D'] = ml_form.clean_L1_D()
            input_dict['L2'] = ml_form.clean_L2()
            input_dict['L3'] = ml_form.clean_L3()
            if model_number in [1, 2]:
                input_dict['hz'] = ml_form.clean_hz()
            else:
                input_dict['Hz'] = ml_form.clean_hz()
            input_dict['Base_Pointers'] = ml_form.clean_Base_Pointers()
            input_dict['Peak_Pointers'] = ml_form.clean_Peak_Pointers()
            input_dict['Memory'] = ml_form.clean_Memory()
            input_dict['cores'] = ml_form.clean_cores()
            input_dict['Nominal'] = ml_form.clean_Nominal()


            base_ = []
            peak_ = []
            # print(L1_D)

            input_data = pd.DataFrame(input_dict, index=[0])
            if model_number in [1, 2]:

                input_data = pd.DataFrame(input_dict, index=[0])
                if model_number == 2:
                    base_model = joblib.load('raw_data/data/SKL/{}_base_{}.pkl'.format(task_number, model_))
                else:
                    base_model = joblib.load('raw_data/data/SKL/{}_base_{}.joblib'.format(task_number, model_))
                if task_number != 4:
                    peak_model = joblib.load('raw_data/data/SKL/{}_peak_{}.joblib'.format(task_number, model_))
                    predictions_peak = peak_model.predict(input_data)[0]
                    peak_.append(predictions_peak)
                    print(predictions_peak)
                predictions = base_model.predict(input_data)[0]
                base_.append(predictions)
                print(predictions)

            else:
                input_data = np.array(input_data)
                input_data = torch.tensor(input_data, dtype=torch.double)
                base_model = MLP_base()
                peak_model = MLP_base()
                base_model.load_state_dict(torch.load(MLP_list[task_number][0]))
                base_model = base_model.double()
                base_model.eval()
                if task_number != 4:
                    peak_model.load_state_dict(torch.load(MLP_list[task_number][1]))
                    peak_model = peak_model.double()
                    peak_model.eval()
                    predictions_peak = peak_model(input_data)
                    predictions_peak = predictions_peak.item()
                predictions = base_model(input_data)
                predictions = predictions.item()

            context['ml_form'] = ml_form
            context['base'] = predictions
            context['peak'] = predictions_peak if task_number != 4 else None
            if task_number != 4 and predictions > predictions_peak:
                context['base'] = predictions_peak
                context['peak'] = predictions

            return render(request, 'mlPredict.html', context)
    else:
        ml_form = MLFrom()
        context['ml_form'] = ml_form
    return render(request, 'mlPredict.html', context)


def predict_tree(request):
    pass


def save_OS(request):
    for key, item in os_dict.items():
        tmp_os = OS.objects.create(OS_name=key, OS_value=item)
        tmp_os.save()
    return render(request, 'mlPredict.html', {})


