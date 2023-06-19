import json
import re

import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from joblib import dump
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler

from sklearn.tree import DecisionTreeRegressor
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Value, CharField, IntegerField

from .models import Benchmark, CFP2017_ratediv_result, SPECrate2017_ratediv_fp_score, SPECrate2017_ratediv_int_score, \
    CINT2017_ratediv_result, SPECrate2017_speeddiv_fp_score, CFP2017_speeddiv_result, SPECrate2017_speeddiv_int_score, \
    CINT2017_speeddiv_result, CFP2017_ratediv, CFP2017_speeddiv, CINT2017_ratediv, CINT2017_speeddiv, \
    CINT2017_speeddiv_hard_soft, CFP2017_speeddiv_hard_soft, CINT2017_ratediv_hard_soft, CFP2017_ratediv_hard_soft, \
    improve_peak_base

from utils.decorators import login_required

# Create your views here.
summary_list = {

    1: CFP2017_ratediv,
    2: CFP2017_speeddiv,
    3: CINT2017_ratediv,
    4: CINT2017_speeddiv

}

result_all_dict = {

    1: CFP2017_ratediv_result,
    2: CFP2017_speeddiv_result,
    3: CINT2017_ratediv_result,
    4: CINT2017_speeddiv_result

}

score_list = {

    1: SPECrate2017_ratediv_fp_score,
    2: SPECrate2017_speeddiv_fp_score,
    3: SPECrate2017_ratediv_int_score,
    4: SPECrate2017_speeddiv_int_score

}

hs_list = [None, CFP2017_ratediv_hard_soft, CFP2017_speeddiv_hard_soft, CINT2017_ratediv_hard_soft,
           CINT2017_speeddiv_hard_soft]


def save_benchmark(request):
    # 这里只是存一下benchmark 这个接口大概率是要弃用的
    benchmark_list = {'511.povray_r', '544.nab_r', '520.omnetpp_r', '505.mcf_r', '500.perlbench_r', '619.lbm_s',
                      '531.deepsjeng_r', '631.deepsjeng_s', '527.cam4_r', '620.omnetpp_s', '510.parest_r', '628.pop2_s',
                      '638.imagick_s',
                      '554.roms_r', '621.wrf_s', '507.cactuBSSN_r', '541.leela_r', '649.fotonik3d_s', '538.imagick_r',
                      '523.xalancbmk_r', '603.bwaves_s', '521.wrf_r', '605.mcf_s', '623.xalancbmk_s', '657.xz_s',
                      '625.x264_s',
                      '508.namd_r', '502.gcc_r', '600.perlbench_s', '648.exchange2_s', '526.blender_r',
                      '607.cactuBSSN_s',
                      '525.x264_r', '519.lbm_r', '557.xz_r', '627.cam4_s', '548.exchange2_r', '644.nab_s',
                      '641.leela_s',
                      '654.roms_s', '503.bwaves_r', '602.gcc_s', '549.fotonik3d_r'}
    for benchmark_ in benchmark_list:
        # print(benchmark_)
        bench = Benchmark.objects.create(benchmark_name=benchmark_)
        bench.save()

    context = {}
    context['fig_1'] = {
        'data': [{'year': "2019", 'data': [200, 200, 300, 900, 1500, 1200, 600]},
                 {'year': "2020", 'data': [300, 400, 350, 800, 1800, 1400, 700]}]
    }
    # context['benchmark_']
    return render(request, 'index.html', context)


def save_CFP2017_ratediv_result(request):
    # 这里只是存一下benchmark 这个接口大概率是要弃用的

    result_file_path = [
        'raw_data/data/result/CFP2017_ratediv_result.json',
        'raw_data/data/result/CFP2017_speeddiv_result.json',
        'raw_data/data/result/CINT2017_ratediv_result.json',
        'raw_data/data/result/CINT2017_speeddiv_result.json'
    ]

    with open('raw_data/data/result/CINT2017_speeddiv_result.json', 'r') as f:
        data = json.load(f)
    print(len(data))
    tt = 0
    for sample in data:
        print(tt)
        tt += 1
        if 'SPECrate\u00ae2017_fp_base' in sample.keys() or 'SPECrate\u00ae2017_int_peak' in sample.keys() \
                or 'SPECrate2017_fp_base' in sample.keys() or 'SPECrate2017_int_peak' in sample.keys() \
                or 'SPECspeed2017_fp_base' in sample.keys() or 'SPECspeed\u00ae2017_fp_base' in sample.keys() \
                or 'SPECspeed2017_int_base' in sample.keys() or 'SPECspeed\u00ae2017_int_base' in sample.keys():
            try:
                p_id = sample['id']
                test_sponsor = sample['test_sponsor']
                System_Name = sample['System_Name']
                # SPECrate2017_fp_base = sample['SPECspeed2017_fp_base'] if 'SPECspeed2017_fp_base' in sample else sample[
                #     'SPECspeed\u00ae2017_fp_base']
                # SPECrate2017_fp_peak = sample['SPECspeed2017_fp_peak'] if 'SPECspeed2017_fp_peak' in sample else sample[
                #     'SPECspeed\u00ae2017_fp_peak']
                # if SPECrate2017_fp_base.strip() == 'Not':
                #     SPECrate2017_fp_base = -1
                # else:
                #     SPECrate2017_fp_base = float(SPECrate2017_fp_base)
                #
                # if SPECrate2017_fp_peak.strip() == 'Not':
                #     SPECrate2017_fp_peak = -1
                # else:
                #     SPECrate2017_fp_peak = float(SPECrate2017_fp_peak)
                # score = SPECrate2017_speeddiv_fp_score.objects.create(
                #     p_id=p_id, test_sponsor=test_sponsor, System_Name=System_Name,
                #     SPECrate2017_fp_base=SPECrate2017_fp_base, SPECrate2017_fp_peak=SPECrate2017_fp_peak
                # )
                # score.save()
                SPECrate2017_int_base = sample['SPECspeed2017_int_base'] if 'SPECspeed2017_int_base' in sample else \
                    sample[
                        'SPECspeed\u00ae2017_int_base']
                SPECrate2017_int_peak = sample['SPECspeed2017_int_peak'] if 'SPECspeed2017_int_peak' in sample else \
                    sample[
                        'SPECspeed\u00ae2017_int_peak']
                if SPECrate2017_int_base.strip() == 'Not':
                    SPECrate2017_int_base = -1
                else:
                    SPECrate2017_int_base = float(SPECrate2017_int_base)

                if SPECrate2017_int_peak.strip() == 'Not':
                    SPECrate2017_int_peak = -1
                else:
                    SPECrate2017_int_peak = float(SPECrate2017_int_peak)

                score = SPECrate2017_speeddiv_int_score.objects.create(
                    p_id=p_id, test_sponsor=test_sponsor, System_Name=System_Name,
                    SPECrate2017_int_base=SPECrate2017_int_base, SPECrate2017_int_peak=SPECrate2017_int_peak
                )
                score.save()

            except Exception as e:
                print(e, sample)
        else:
            # benchmark details
            # {'id': 0, 'test_sponsor': 'ASRock Rack Inc.', 'System_Name': '1U4LW-X570 RPSU AMD Ryzen 7 5800X,3.8GHz',
            # 'benchmark': '527.cam4_r', 'basecol_copies': ['16'], 'basecol_time': ['355', '351'],
            # 'basecol_ratio': ['78.8', '79.7'], 'peakcol_copies': ['16'], 'peakcol_time': ['348', '350'],
            # 'peakcol_ratio': ['80.5', '79.9']}
            # print(sample)
            try:
                p_id = sample['id']
                test_sponsor = sample['test_sponsor'].strip()
                System_Name = sample['System_Name'].strip()
                benchmark = Benchmark.objects.filter(benchmark_name=sample['benchmark'])[0]
                basecol_threads = float(sample['basecol_threads'][0]) if "basecol_threads" in sample else -1
                peakcol_threads = float(sample['peakcol_threads'][0]) if "peakcol_threads" in sample else -1
                # 先base
                # assert len(sample['basecol_ratio']) == len(sample['peakcol_ratio'])
                # 确实是一样多的哈哈哈
                inter = 0
                for i in range(len(sample['basecol_ratio'])):
                    basecol_ratio = float(sample['basecol_ratio'][i]) if "basecol_ratio" in sample else -1
                    basecol_time = float(sample['basecol_time'][i]) if "basecol_time" in sample else -1
                    peakcol_ratio = float(sample['peakcol_ratio'][i]) if "peakcol_ratio" in sample else -1
                    peakcol_time = float(sample['peakcol_time'][i]) if "peakcol_time" in sample else -1
                    turn = inter
                    result = CINT2017_speeddiv_result(
                        p_id=p_id, test_sponsor=test_sponsor, System_Name=System_Name, turn=turn, benchmark=benchmark,
                        basecol_threads=basecol_threads, peakcol_threads=peakcol_threads, basecol_ratio=basecol_ratio,
                        basecol_time=basecol_time, peakcol_ratio=peakcol_ratio, peakcol_time=peakcol_time
                    )
                    result.save()
                    inter += 1
            except Exception as e:
                print(sample)

    context = {}
    context['fig_1'] = {
        'data': [{'year': "2019", 'data': [200, 200, 300, 900, 1500, 1200, 600]},
                 {'year': "2020", 'data': [300, 400, 350, 800, 1800, 1400, 700]}]
    }
    # context['benchmark_']
    return render(request, 'index.html', context)


def result_list(request, table_number, page_number):
    summary_name_list = {

        1: 'CFP2017_rate',
        2: 'CFP2017_speed',
        3: 'CINT2017_rate',
        4: 'CINT2017_speed'

    }
    summary = summary_list[table_number].objects.all()
    paginator = Paginator(summary, 30)  # 每页显示10条数据
    t_page = request.GET.get('page')
    if t_page is not None:
        page_number = t_page
    summary_obj = paginator.get_page(page_number)
    context = {'summary_obj': summary_obj, 'table_number': table_number, 't_page': t_page,
               'summary_name_list': summary_name_list}
    # return render(request, 'my_template.html', {})
    return render(request, 'index_1.html', context)


@login_required
def details(request, table_number, p_id):
    # 先把数据都提取出来
    summary_name_list = {

        1: 'CFP2017_rate',
        2: 'CFP2017_speed',
        3: 'CINT2017_rate',
        4: 'CINT2017_speed'

    }
    summary = summary_list[table_number].objects.filter(p_id=p_id)[0]
    result = result_all_dict[table_number].objects.filter(p_id=p_id)
    score = score_list[table_number].objects.filter(p_id=p_id)[0]
    hard_soft_ware = hs_list[table_number].objects.filter(p_id=p_id)[0]

    # print(len(summary))
    # print(len(result))
    # print(len(score))
    # print(len(hard_soft_ware))

    # format the data
    result_dict = {}
    score_dict = {}

    if table_number in [1, 3]:

        for obj in result:
            if obj.benchmark.benchmark_name not in result_dict:
                result_dict[obj.benchmark.benchmark_name] = {'base': [], 'peak': [], 'base_copies': obj.basecol_copies,
                                                             'peak_copies': obj.peakcol_copies}
            basecol_ratio = obj.basecol_ratio
            if obj.basecol_ratio % 10 == 0.0:
                basecol_ratio = obj.basecol_ratio / 10
            peakcol_ratio = obj.peakcol_ratio
            if obj.peakcol_ratio % 10 == 0.0:
                peakcol_ratio = obj.peakcol_ratio / 10

            basecol_time = obj.basecol_time
            if obj.basecol_ratio % 10 == 0.0:
                basecol_time = obj.basecol_time / 10
            peakcol_time = obj.peakcol_time
            if obj.peakcol_time % 10 == 0.0:
                peakcol_time = obj.peakcol_time / 10
            result_dict[obj.benchmark.benchmark_name]['base'].append([basecol_time, basecol_ratio])
            result_dict[obj.benchmark.benchmark_name]['peak'].append([peakcol_time, peakcol_ratio])

    else:

        for obj in result:
            if obj.benchmark.benchmark_name not in result_dict:
                result_dict[obj.benchmark.benchmark_name] = {'base': [], 'peak': [], 'base_copies': obj.basecol_threads,
                                                             'peak_copies': obj.peakcol_threads}
            basecol_ratio = obj.basecol_ratio
            if obj.basecol_ratio % 10 == 0.0:
                basecol_ratio = obj.basecol_ratio / 10
            peakcol_ratio = obj.peakcol_ratio
            if obj.peakcol_ratio % 10 == 0.0:
                peakcol_ratio = obj.peakcol_ratio / 10

            basecol_time = obj.basecol_time
            if int(obj.basecol_time) % 10 == 0:
                print(obj.basecol_time)
                basecol_time = obj.basecol_time / 10
            peakcol_time = obj.peakcol_time
            if int(obj.peakcol_time) % 10 == 0:
                peakcol_time = obj.peakcol_time / 10

            result_dict[obj.benchmark.benchmark_name]['base'].append([basecol_time, basecol_ratio])
            result_dict[obj.benchmark.benchmark_name]['peak'].append([peakcol_time, peakcol_ratio])
    for benchm, item in result_dict.items():
        for key in result_dict[benchm].keys():
            if isinstance(result_dict[benchm][key], list) and len(result_dict[benchm][key]) > 3:
                result_dict[benchm][key] = result_dict[benchm][key][:3]
    if table_number in [1, 2]:
        score_dict["base"] = score.SPECrate2017_fp_base
        score_dict["peak"] = score.SPECrate2017_fp_peak
    else:
        score_dict["base"] = score.SPECrate2017_int_base
        score_dict["peak"] = score.SPECrate2017_int_peak
    # print(result_dict)
    hs_dict = {}

    summary_dict = {}
    for field in summary._meta.get_fields():
        field_name = field.name
        if field_name == 'id':
            continue

        field_value = getattr(summary, field_name)
        if field_value is not None and field_value != 'None':
            if isinstance(field_value, float) or isinstance(field_value, int):
                if field_value <= 0:
                    continue
            summary_dict[field_name] = field_value

    for field in hard_soft_ware._meta.get_fields():
        field_name = field.name
        if field_name == 'id' or field_name == 'p_id':
            continue
        field_value = getattr(hard_soft_ware, field_name)
        if field_value is not None and field_value != 'None':
            hs_dict[field_name] = field_value

    half_len = len(hs_dict) // 2
    dict1 = {k: v for i, (k, v) in enumerate(hs_dict.items()) if i < half_len}
    dict2 = {k: v for i, (k, v) in enumerate(hs_dict.items()) if i >= half_len}
    context = {
        'summary': summary,
        'result_dict': result_dict,
        'score_dict': score_dict,
        'hs_dict_1': dict1,
        'hs_dict_2': dict2,
        'summary_name_list': summary_name_list
    }
    return render(request, 'details.html', context)


def clean_data(request):
    # 把result洗一下
    # float
    pass


@login_required
def search(request, keywords, page_number):
    summary_name_list = {

        1: 'CFP2017_rate',
        2: 'CFP2017_speed',
        3: 'CINT2017_rate',
        4: 'CINT2017_speed'

    }
    # for key, task in summary_name_list:
    #     pass
    if keywords == "333":
        keywords = request.GET.get('search')
    keywords = str(keywords).strip()
    results = []

    if keywords and keywords != "":
        for key, task in summary_list.items():
            results_tmp = task.objects.filter(Q(test_sponsor__icontains=keywords) | Q(System_Name__icontains=keywords))

            results_tmp = results_tmp.annotate(task=Value(key, output_field=IntegerField()))

            results.extend(results_tmp)

    paginator = Paginator(results, 30)  # 每页显示30条数据
    t_page = request.GET.get('page')
    if t_page is not None:
        page_number = t_page
    summary_obj = paginator.get_page(page_number)
    context = {'t_page': t_page,
               'summary_name_list': summary_name_list, 'keywords': keywords, 'summary_obj': summary_obj}

    return render(request, 'search.html', context)


def hs_su(request):
    os_set = set()
    total = 0
    to_2 = 0
    for hs in hs_list[1:]:
        hs_res_list = hs.objects.all()
        total += len(hs_res_list)
        for obj in hs_res_list:
            os_set.add(obj.OS.strip())
    for key, item in result_all_dict.items():
        tt = item.objects.all()
        to_2 += len(tt)
    print(len(os_set))
    print("total", total)
    print("to_2", to_2)
    return render(request, 'dataspace.html', {})


def data_create(request):
    summary_name_list = {

        1: 'CFP2017_rate',
        2: 'CFP2017_speed',
        3: 'CINT2017_rate',
        4: 'CINT2017_speed'

    }
    os_dict = {}
    os_poi = 0
    for hs in hs_list[1:]:
        hs_res_list = hs.objects.all()
        for obj in hs_res_list:
            if obj.OS.strip() not in os_dict:
                os_dict[obj.OS.strip()] = os_poi
                os_poi += 1
    for i in range(1, 5):
        print(i)
        choose = i
        summary = summary_list[choose].objects.all()
        train_dataset = []
        p_l1 = re.compile('([1-9]+) KB I \+ ([1-9]+) KB D on chip per core')
        p_l2 = re.compile('([1-9]+) ([K|M])B')
        p_memory = re.compile('([1-9]+) ([T|G])')
        print("summary", len(summary))

        for obj in summary:
            tmp_dict = {}
            p_id = obj.p_id
            score = score_list[choose].objects.filter(p_id=p_id)
            if len(score) == 0:
                continue
            score = score[0]
            hs_ware = hs_list[choose].objects.filter(p_id=p_id)[0]
            if choose in [1, 2]:
                tmp_dict["base"] = score.SPECrate2017_fp_base
                tmp_dict["peak"] = score.SPECrate2017_fp_peak
            else:
                tmp_dict["base"] = score.SPECrate2017_int_base
                if choose == 3:
                    tmp_dict["peak"] = score.SPECrate2017_int_peak


            # print(tmp_dict)
            tmp_dict['hz'] = hs_ware.Max_MHz
            tmp_dict['L1'] = hs_ware.Cache_L1
            L1_res = re.findall(p_l1, tmp_dict['L1'])
            tmp_dict['L2'] = hs_ware.Cache_L2
            tmp_dict['L3'] = hs_ware.Cache_L3
            cores_ = hs_ware.Enabled
            tmp_dict['Nominal'] = int(hs_ware.Nominal)
            p_core = re.compile('([0-9]+)* *cores')
            try:
                tmp_dict['cores'] = re.findall(p_core, cores_)[0]
                # print(tmp_dict['cores'])
                tmp_dict['cores'] = int(tmp_dict['cores'].strip())
            except Exception as e:
                print(cores_)
                continue


            L2_res = re.findall(p_l2, tmp_dict['L2'])
            L3_res = re.findall(p_l2, tmp_dict['L3'])
            if len(L1_res) == 0 or len(L2_res) == 0 or len(L3_res) == 0:
                # print(tmp_dict['L1'])
                continue
            tmp_dict['L1_I'] = int(L1_res[0][0])
            tmp_dict['L1_D'] = int(L1_res[0][1])

            tmp_dict['L3'] = int(L3_res[0][0]) * 1024 if L3_res[0][1] != '' and L3_res[0][1] == 'M' else int(
                L3_res[0][0])
            tmp_dict['L2'] = int(L2_res[0][0]) * 1024 if L2_res[0][1] != '' and L2_res[0][1] == 'M' else int(
                L2_res[0][0])

            tmp_dict["Base_Pointers"] = hs_ware.Base_Pointers
            tmp_dict["Peak_Pointers"] = hs_ware.Peak_Pointers
            mem_res = re.findall(p_memory, hs_ware.Memory)
            if len(mem_res) == 0:
                continue
            tmp_dict["Memory"] = int(mem_res[0][0]) * 1024 if mem_res[0][1] == 'T' else int(mem_res[0][0])
            tmp_dict['OS'] = os_dict[hs_ware.OS.strip()]
            # print(tmp_dict)
            train_dataset.append(tmp_dict)
        print(summary_name_list[choose], len(train_dataset))
        with open("raw_data/data/SKL/{}.json".format(summary_name_list[choose]), "w+") as f:
            json.dump(train_dataset, f, ensure_ascii=False)

    return render(request, 'dataspace.html', {})


def train_SVM(request):
    summary_name_list = {

        1: 'CFP2017_rate',
        2: 'CFP2017_speed',
        3: 'CINT2017_rate',
        4: 'CINT2017_speed'

    }
    for i in range(1, 5):
        print(i)
        choose = i

        file_path = "raw_data/data/SKL/%s.json" % summary_name_list[choose]
        base_data = []
        peak_data = []
        with open(file_path, 'r') as file:
            data_ = file.read()
            data_ = json.loads(data_)
            for data in data_:
                if data['base'] > 0 and data['peak'] > 0:
                    base_data.append(data)
                if choose != 4 and data['peak'] > 0:
                    peak_data.append(data)

        # print(data[1])

        base_data = pd.DataFrame(base_data)

        if choose != 4:
            peak_data = pd.DataFrame(peak_data)
            X_peak = peak_data[
                ['L1_I', 'L1_D', 'L2', 'L3', 'hz', "Base_Pointers", 'Peak_Pointers', 'Memory', 'cores', 'Nominal']]
            # 特征列（输入）
            peak = peak_data['peak']  # 目标列（输出）

        print(base_data[:10])
        X = base_data[['L1_I', 'L1_D', 'L2', 'L3', 'hz', "Base_Pointers", 'Peak_Pointers', 'Memory', 'cores', 'Nominal']]  # 特征列（输入）

        base = base_data['base']  # 目标列（输出）

        # 对DataFrame的所有列进行归一化操作


        X_train, X_test, y_train, y_test = train_test_split(X, base, test_size=0.2, random_state=42)
        model = SVR(C=10, kernel='rbf', gamma=1)
        print(y_train)
        # # 使用训练集进行模型训练
        model.fit(X_train, y_train)

        # 使用测试集进行预测
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)

        # 计算决定系数
        r2 = r2_score(y_test, predictions)

        print("Mean Squared Error: {:.2f}".format(mse))
        print("R-squared: {:.2f}".format(r2))
        # param_grid = {
        #     'svm__C': [0.1, 1, 10],
        #     'svm__kernel': ['linear', 'poly', 'rbf'],
        #     'svm__gamma': [0.1, 1, 10]
        # }
        # # 创建Pipeline对象，包括数据预处理和模型
        # pipeline = Pipeline([
        #     ('scaler', StandardScaler()),
        #     ('svm', model)
        # ])
        #
        # # 创建GridSearchCV对象，传入模型、参数网格和评估指标
        # grid_search = GridSearchCV(pipeline, param_grid=param_grid, scoring='neg_mean_squared_error', cv=5)
        #
        # # 使用训练数据进行网格搜索和交叉验证
        # grid_search.fit(X_train, y_train)
        dump(model, 'raw_data/data/SKL/{}_base_svm_regression_model_{:.2f}.joblib'.format(choose, r2))
        if choose != 4:
            X_train_peak, X_test_peak, y_train_peak, y_test_peak = train_test_split(X_peak, peak,
                                                                                    test_size=0.2, random_state=42)
            model.fit(X_train_peak, y_train_peak)

            predictions = model.predict(X_test_peak)
            mse = mean_squared_error(y_test_peak, predictions)

            # 计算决定系数
            r2 = r2_score(y_test_peak, predictions)

            print("Mean Squared Error: {:.2f}".format(mse))
            print("R-squared: {:.2f}".format(r2))
            dump(model, 'raw_data/data/SKL/{}_peak_svm_regression_model_{:.2f}.joblib'.format(choose, r2))
    return render(request, 'dataspace.html', {})


def train_tree(request):
    summary_name_list = {

        1: 'CFP2017_rate',
        2: 'CFP2017_speed',
        3: 'CINT2017_rate',
        4: 'CINT2017_speed'

    }
    for i in range(1, 5):
        print(i)
        choose = i

        file_path = "raw_data/data/SKL/%s.json" % summary_name_list[choose]
        base_data = []
        peak_data = []
        with open(file_path, 'r') as file:
            data_ = file.read()
            data_ = json.loads(data_)
            for data in data_:
                if data['base'] > 0:
                    base_data.append(data)
                if choose != 4 and data['peak'] > 0:
                    peak_data.append(data)

        # print(data[1])

        base_data = pd.DataFrame(base_data)
        scaler = MinMaxScaler()
        if choose != 4:
            peak_data = pd.DataFrame(peak_data)
            X_peak = peak_data[
                ['L1_I', 'L1_D', 'L2', 'L3', 'hz', "Base_Pointers", 'Peak_Pointers', 'Memory', 'cores', 'Nominal']]  # 特征列（输入）
            peak = peak_data['peak']  # 目标列（输出）
            normalized_data_peak = scaler.fit_transform(X_peak)
        print(base_data[:10])
        X = base_data[['L1_I', 'L1_D', 'L2', 'L3', 'hz', "Base_Pointers", 'Peak_Pointers', 'Memory', 'cores', 'Nominal']]  # 特征列（输入）

        base = base_data['base']  # 目标列（输出）

        # 对DataFrame的所有列进行归一化操作
        normalized_data = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(normalized_data, base, test_size=0.2, random_state=42)
        model = DecisionTreeRegressor()
        print(y_train)
        # # 使用训练集进行模型训练
        model.fit(X_train, y_train)

        # 使用测试集进行预测
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)

        # 计算决定系数
        r2 = r2_score(y_test, predictions)

        print("Mean Squared Error: {:.2f}".format(mse))
        print("R-squared: {:.2f}".format(r2))
        # param_grid = {
        #     'svm__C': [0.1, 1, 10],
        #     'svm__kernel': ['linear', 'poly', 'rbf'],
        #     'svm__gamma': [0.1, 1, 10]
        # }
        # # 创建Pipeline对象，包括数据预处理和模型
        # pipeline = Pipeline([
        #     ('scaler', StandardScaler()),
        #     ('svm', model)
        # ])
        #
        # # 创建GridSearchCV对象，传入模型、参数网格和评估指标
        # grid_search = GridSearchCV(pipeline, param_grid=param_grid, scoring='neg_mean_squared_error', cv=5)
        #
        # # 使用训练数据进行网格搜索和交叉验证
        # grid_search.fit(X_train, y_train)
        dump(model, 'raw_data/data/SKL/{}_base_DecisionTreeRegressor_{:.2f}.train_tree'.format(choose, r2))
        if choose != 4:
            X_train_peak, X_test_peak, y_train_peak, y_test_peak = train_test_split(normalized_data_peak, peak,
                                                                                    test_size=0.2, random_state=42)
            model.fit(X_train_peak, y_train_peak)

            predictions = model.predict(X_test_peak)
            mse = mean_squared_error(y_test_peak, predictions)

            # 计算决定系数
            r2 = r2_score(y_test_peak, predictions)

            print("Mean Squared Error: {:.2f}".format(mse))
            print("R-squared: {:.2f}".format(r2))
            dump(model, 'raw_data/data/SKL/{}_peak_DecisionTreeRegressor_{:.2f}.joblib'.format(choose, r2))
    return render(request, 'dataspace.html', {})


def summary_hard_soft_improve(request):
    for key in summary_list.keys():
        summary_ = summary_list[key].objects.all()
        sponsor_dict = {}
        for obj in summary_:
            score = score_list[key].objects.filter(p_id=obj.p_id)
            if len(score) == 0:
                continue
            score = score[0]
            if key in [1, 2]:
                peak = score.SPECrate2017_fp_peak
                base = score.SPECrate2017_fp_base
            else:
                peak = score.SPECrate2017_int_peak
                base = score.SPECrate2017_int_base
            if peak <= 0 or base <= 0:
                continue
            test_sponsor = obj.test_sponsor
            if test_sponsor not in sponsor_dict:
                sponsor_dict[test_sponsor] = []

            sponsor_dict[test_sponsor].append(peak - base)
        print("summary_ complete")
        for k, score_item in sponsor_dict.items():
            improve_score = sum(sponsor_dict[k]) / len(score_item)
            improve = improve_peak_base.objects.create(test_sponsor=k, improve_score=improve_score, task=key)
            improve.save()
        print("key %s complete" % key)
    return render(request, 'dataspace.html', {})
