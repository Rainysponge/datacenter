import re
import json
import numpy as np

from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.db import models
from django.core.cache import cache

from django.db.models import Case, Count, IntegerField, When

from dataspace.models import CFP2017_ratediv, CFP2017_speeddiv, CINT2017_ratediv, CINT2017_speeddiv, \
    SPECrate2017_speeddiv_int_score, SPECrate2017_ratediv_int_score, SPECrate2017_ratediv_fp_score, \
    SPECrate2017_speeddiv_fp_score, CFP2017_ratediv_hard_soft, CFP2017_speeddiv_hard_soft, CINT2017_ratediv_hard_soft, \
    CINT2017_speeddiv_hard_soft, improve_peak_base

summary_list = {

    "FP_rate": CFP2017_ratediv,
    "FP_speed": CFP2017_speeddiv,
    "INT_rate": CINT2017_ratediv,
    "INT_speed": CINT2017_speeddiv

}

score_list = {
    "FP_rate": SPECrate2017_ratediv_fp_score,
    "FP_speed": SPECrate2017_speeddiv_fp_score,
    "INT_rate": SPECrate2017_ratediv_int_score,
    "INT_speed": SPECrate2017_speeddiv_int_score
}

hs_ware_list = {
    "FP_rate": CFP2017_ratediv_hard_soft,
    "FP_speed": CFP2017_speeddiv_hard_soft,
    "INT_rate": CINT2017_ratediv_hard_soft,
    "INT_speed": CINT2017_speeddiv_hard_soft
}


def home(request):
    context = cache.get('my_data')
    # context = None
    if context is None:
        fig_1_key_list, fig_1_data = fig_1()
        fig_score_dis_key_list, fig_score_dis_data = fig_score_dis()
        fig_6_pie_dict, fig_6_pie_data = fig_sponsor_pie()
        fig_hz_key_list, fig_hz_data = fig_Hz()
        fig_core_score_key_list, fig_core_score_data = fig_core_score()
        fig_hz_score_key_list, fig_hz_score_data = fig_hz_score()
        fig_improve_key_list, fig_improve_data = fig_improve()
        context = {}
        context['fig_1_key_list'] = list(fig_1_key_list)
        context['fig_1_data'] = fig_1_data

        context['fig_score_dis_data'] = fig_score_dis_data

        # context['fig_6_pie_dict'] = list(fig_6_pie_dict)
        context['fig_6_pie_data'] = fig_6_pie_data

        # context['fig_hz_key_list'] = list(fig_hz_key_list)
        context['fig_hz_data'] = fig_hz_data
        context['fig_hz_score_data'] = fig_hz_score_data

        # context['fig_core_score_key_list'] = list(fig_core_score_key_list)
        context['fig_core_score_data'] = fig_core_score_data
        context['fig_hz_score_data'] = fig_hz_score_data
        context['fig_improve_data'] = fig_improve_data

        cache.set('my_data', context, timeout=1800)
    # context = get_data()
    return render(request, 'index.html', context)


def fig_1():
    # 按照每个任务统计个数
    data = {"data": [], "data_pie": []}
    fig_1_company_number = {}
    summary_number = {}
    for key in summary_list:
        summary = summary_list[key]
        test_sponsor = summary.objects.values('test_sponsor') \
            .annotate(count=models.Count('test_sponsor'))

        tmp_dict = {item['test_sponsor'].strip(): item['count'] for item in test_sponsor}
        # res_dict = {}
        # res_dict['summary'] = key
        for k, item in tmp_dict.items():
            summary_number[k] = item if k not in summary_number else summary_number[k] + item
        fig_1_company_number[key] = tmp_dict
    keys_list = dict(sorted(summary_number.items(), key=lambda x: x[1], reverse=True)[:6]).keys()  # 这个是要return的

    for key in summary_list:
        tmp_dict = {}
        tmp_dict_2 = {}

        tmp_dict['year'] = key
        tmp_dict_2['year'] = key

        tmp_dict['data'] = []
        tmp_dict_2['data'] = []
        total = 0
        get = 0

        for k in keys_list:
            get += fig_1_company_number[key][k]
            tmp_dict['data'].append(fig_1_company_number[key][k])
            tmp_dict_2['data'].append(fig_1_company_number[key][k])

        for k in keys_list:
            total += fig_1_company_number[key][k]

        data['data'].append(tmp_dict)
    return keys_list, data


def fig_sponsor_pie():
    data = {"data": []}
    fig_1_company_number = {}

    keys_dict = {}
    total = {}
    for key in summary_list:
        summary = summary_list[key]
        test_sponsor = summary.objects.values('test_sponsor') \
            .annotate(count=models.Count('test_sponsor'))

        tmp_dict = {item['test_sponsor'].strip(): item['count'] for item in test_sponsor}
        # res_dict = {}
        # res_dict['summary'] = key
        tmp_total = 0
        for k, item in tmp_dict.items():
            tmp_total += item
        total[key] = tmp_total
        fig_1_company_number[key] = tmp_dict
        keys_dict[key] = dict(sorted(fig_1_company_number[key].items(), key=lambda x: x[1], reverse=True)[:7]).keys()

    for key in summary_list:
        key_list = keys_dict[key]

        tmp_dict = {'year': key}
        tmp_dict['data'] = {}  # pie图需要键值对应
        get = 0  # 记录被选中的个数，为了和others做区分
        for k in key_list:
            get += fig_1_company_number[key][k]
            tmp_dict['data'][k] = fig_1_company_number[key][k]
        tmp_dict['data']['others'] = total[key] - get
        data["data"].append(tmp_dict)

    return keys_dict, data


def fig_score_dis():
    # 折线图 peak 需要遍历一下
    key_list = []
    data = []  # data = [{year: "xxx", data:[[], []]}]
    min_base = 999999
    min_peak = 999999
    max_base = 0.0
    max_peak = 0.0
    # 后端统计下吧
    for key, item in score_list.items():
        key_list.append(key)
        tmp_dict = {'year': key, 'data': [[], [], []]}
        if key in ["FP_rate", "FP_speed"]:

            data_base = item.objects.exclude(SPECrate2017_fp_base=-1.0)
            data_peak = item.objects.exclude(SPECrate2017_fp_peak=-1.0)
            for obj in data_base:
                tmp_dict['data'][0].append(obj.SPECrate2017_fp_base)
                min_base = min(min_base, obj.SPECrate2017_fp_base)
                max_base = max(max_base, obj.SPECrate2017_fp_base)
            for obj in data_peak:
                tmp_dict['data'][1].append(obj.SPECrate2017_fp_peak)
                min_peak = min(min_peak, obj.SPECrate2017_fp_peak)
                max_peak = max(max_peak, obj.SPECrate2017_fp_peak)
            min_ = min(min_base, min_peak)
            max_ = min(max_base, max_peak)
        else:
            data_base = item.objects.exclude(SPECrate2017_int_base=-1.0)
            data_peak = item.objects.exclude(SPECrate2017_int_peak=-1.0)
            for obj in data_base:
                tmp_dict['data'][0].append(obj.SPECrate2017_int_base)
                min_base = min(min_base, obj.SPECrate2017_int_base)
                max_base = max(max_base, obj.SPECrate2017_int_base)
            for obj in data_peak:
                tmp_dict['data'][1].append(obj.SPECrate2017_int_peak)
                min_peak = min(min_peak, obj.SPECrate2017_int_peak)
                max_peak = max(max_peak, obj.SPECrate2017_int_peak)
            min_ = min(min_base, min_peak)
            max_ = min(max_base, max_peak)
        # 我们已经有了最大最小值 划分成30个等距区间

        min_value = min_
        max_value = max_

        # 定义区间的数量
        num_intervals = 30

        # 构建区间边界数组
        interval_boundaries = np.linspace(min_value, max_value, num=num_intervals + 1)

        # 分配数据到区间中
        interval_base_counts = np.histogram(tmp_dict['data'][0], bins=interval_boundaries)[0]
        interval_peak_counts = np.histogram(tmp_dict['data'][1], bins=interval_boundaries)[0]
        tmp_dict['data'][0] = list()
        tmp_dict['data'][1] = list()
        # 打印每个区间的统计数量
        for i in range(num_intervals):
            start = interval_boundaries[i]
            end = interval_boundaries[i + 1]

            tmp_dict['data'][0].append(round((start + end) / 2))
            tmp_dict['data'][1].append(interval_base_counts[i])
            tmp_dict['data'][2].append(interval_peak_counts[i])
        data.append(tmp_dict)
    # print(data)

    return key_list, data


def fig_Hz():
    # 我想用柱状图表示先看效果 频率
    # 只需要统计
    key_list = []
    data = []  # [{year: "xx", 'data':[123,123]},]
    for key, item in hs_ware_list.items():
        tmp_dict = {'year': key, 'data': [[], [], []]}
        max_hz = item.objects.filter(Max_MHz__gt=0).values_list('Max_MHz', flat=True)
        total = len(max_hz)
        min_, max_ = 999999, -1
        for hz_item in max_hz:
            min_ = min(min_, hz_item)
            max_ = max(max_, hz_item)

        num_intervals = 5
        interval_boundaries = np.linspace(min_, max_, num=num_intervals + 1)
        interval_hz = np.histogram(max_hz, bins=interval_boundaries)[0]
        # print(interval_hz)
        for i in range(num_intervals):
            start = interval_boundaries[i]
            end = interval_boundaries[i + 1]
            tmp_dict['data'][0].append(round((start + end) / 2))
            tmp_dict['data'][1].append(interval_hz[i])
            tmp_dict['data'][2].append(round(interval_hz[i] / total * 100))

        data.append(tmp_dict)
    return key_list, data


def fig_core_score():
    key_list = []
    data = []

    for key in score_list.keys():
        key_list.append(key)
        score_class = score_list[key]
        hs_ware_class = hs_ware_list[key]
        score_base = None
        score_peak = None
        base_pid = []
        peak_pid = []
        base_score = {}
        peak_score = {}
        if key in ["FP_rate", "FP_speed"]:

            score_base = score_class.objects.filter(SPECrate2017_fp_base__gt=0.0)
            score_peak = score_class.objects.filter(SPECrate2017_fp_peak__gt=0.0)
            for obj in score_base:
                base_score[obj.p_id] = obj.SPECrate2017_fp_base
                # base_score.append(obj.SPECrate2017_fp_peak)
            for obj in score_peak:
                peak_score[obj.p_id] = obj.SPECrate2017_fp_peak


        else:
            score_base = score_class.objects.filter(SPECrate2017_int_base__gt=0.0)
            score_peak = score_class.objects.filter(SPECrate2017_int_peak__gt=0.0)
            for obj in score_base:
                base_score[obj.p_id] = obj.SPECrate2017_int_base
                # base_score.append(obj.SPECrate2017_fp_peak)
            for obj in score_peak:
                peak_score[obj.p_id] = obj.SPECrate2017_int_peak
        # print(score_base)
        for obj in score_base:
            base_pid.append(obj.p_id)

        for obj in score_peak:
            peak_pid.append(obj.p_id)
        total_pid = list(set(base_pid) & set(peak_pid))
        # core - score
        hs_ware = hs_ware_class.objects.filter(p_id__in=total_pid)

        core_number_dict = {}

        p = re.compile('(.*?)core')
        for obj in hs_ware:
            p_id = obj.p_id
            core_ = obj.Enabled

            core_l = re.findall(p, core_)

            if len(core_l) > 0:
                core_l = int(core_l[0].strip())
            else:
                print(core_)
                continue  # clean数据
            core_number_dict[p_id] = core_l
            # hz_dict
        core_score = {}  # {'key': [[],[]]}

        for k, item in core_number_dict.items():

            if item not in core_score:
                core_score[item] = [[], []]
            core_score[item][0].append(base_score[k])
            core_score[item][1].append(peak_score[k])
        for k, item in core_score.items():
            core_score[k][0] = sum(core_score[k][0]) / len(core_score[k][0])  # 计算均值
            core_score[k][1] = sum(core_score[k][1]) / len(core_score[k][1])
        # for k, item in core_number_dict:
        # 整理下数据
        tmp_dict = {'year': key, 'data': [[], [], []]}
        core_s2b = sorted(core_score.keys())
        for k in core_s2b:
            tmp_dict['data'][0].append(k)
            tmp_dict['data'][1].append(core_score[k][0])
            tmp_dict['data'][2].append(core_score[k][1])
        # print(key, tmp_dict)
        data.append(tmp_dict)

    return key_list, data


def fig_hz_score():
    key_list = []
    data = []

    for key in score_list.keys():
        key_list.append(key)
        score_class = score_list[key]
        hs_ware_class = hs_ware_list[key]
        score_base = None
        score_peak = None
        base_pid = []
        peak_pid = []
        base_score = {}
        peak_score = {}
        if key in ["FP_rate", "FP_speed"]:

            score_base = score_class.objects.filter(SPECrate2017_fp_base__gt=0.0)
            score_peak = score_class.objects.filter(SPECrate2017_fp_peak__gt=0.0)
            for obj in score_base:
                base_score[obj.p_id] = obj.SPECrate2017_fp_base
                # base_score.append(obj.SPECrate2017_fp_peak)
            for obj in score_peak:
                peak_score[obj.p_id] = obj.SPECrate2017_fp_peak


        else:
            score_base = score_class.objects.filter(SPECrate2017_int_base__gt=0.0)
            score_peak = score_class.objects.filter(SPECrate2017_int_peak__gt=0.0)
            for obj in score_base:
                base_score[obj.p_id] = obj.SPECrate2017_int_base
                # base_score.append(obj.SPECrate2017_fp_peak)
            for obj in score_peak:
                peak_score[obj.p_id] = obj.SPECrate2017_int_peak
        # print(score_base)
        for obj in score_base:
            base_pid.append(obj.p_id)

        for obj in score_peak:
            peak_pid.append(obj.p_id)
        total_pid = list(set(base_pid) & set(peak_pid))
        # core - score
        hs_ware = hs_ware_class.objects.filter(p_id__in=total_pid, Max_MHz__gt=0)
        hz_score_dict = {}
        for obj in hs_ware:
            p_id = obj.p_id
            hz_ = obj.Max_MHz
            if hz_ not in hz_score_dict:
                hz_score_dict[hz_] = [[], []]
            base_ = base_score[p_id]
            peak_ = peak_score[p_id]
            hz_score_dict[hz_][0].append(base_)
            hz_score_dict[hz_][1].append(peak_)
        # print(hz_score_dict)
        for k, item in hz_score_dict.items():
            hz_score_dict[k][0] = sum(hz_score_dict[k][0]) / len(hz_score_dict[k][0])
            hz_score_dict[k][1] = sum(hz_score_dict[k][1]) / len(hz_score_dict[k][1])
        tmp_dict = {'year': key, 'data': [[], [], []]}
        core_s2b = sorted(hz_score_dict.keys())
        for k in core_s2b:
            tmp_dict['data'][0].append(k)
            tmp_dict['data'][1].append(hz_score_dict[k][0])
            tmp_dict['data'][2].append(hz_score_dict[k][1])
        print(key, tmp_dict)
        data.append(tmp_dict)

    return key_list, data


def home_2(request):
    user = request.user

    context = {}

    return render(request, "index_1.html", context)


def fig_improve():
    # improve_peak_base
    data = []
    key_list = []
    task_list = {
        1: "FP_rate",
        2: "FP_speed",
        3: "INT_rate",
        4: "INT_speed"
    }
    for task in range(1, 5):
        sponsor_dict = {}
        improve = improve_peak_base.objects.filter(task=task)
        for obj in improve:
            sponsor_dict[obj.test_sponsor] = obj.improve_score
        sorted_dict = dict(sorted(sponsor_dict.items(), key=lambda x: x[1], reverse=True))
        # 判断下个数
        x = []
        y = []
        num = 0
        for key, item in sorted_dict.items():
            x.append(key)
            y.append(item)
            num += 1
            if num > 5:
                break
        data.append({"year": task_list[task], 'data': [x, y]})
    print(data)
    return key_list, data
