import re
import json

import pymysql

# 读取数据
file_path_list = [
    'raw_data/data/CFP2017_ratediv.json',
    'raw_data/data/CFP2017_speeddiv.json',
    'raw_data/data/CINT2017_ratediv.json',
    'raw_data/data/CINT2017_speeddiv.json',

]

sh_file_path_list = [
    'raw_data/data/CFP2017_ratedivhard_software.json',
    'raw_data/data/CFP2017_speeddivhard_software.json',
    'raw_data/data/CINT2017_ratedivhard_software.json',
    'raw_data/data/CINT2017_speeddivhard_software.json',
]

res_file_path_list = [
    'raw_data/data/result/CFP2017_ratediv_result.json',
    'raw_data/data/result/CFP2017_speeddiv_result.json',
    'raw_data/data/result/CINT2017_ratediv_result.json',
    'raw_data/data/result/CINT2017_speeddiv_result.json',
]


def clean_CFP2017_ratediv_data():
    table = file_path_list[0].split('/')[-1].split('.')[0]
    print(table)
    with open(file_path_list[0], 'r') as f:
        data = json.load(f)

    for sample in data:
        sample['p_id'] = sample['id']

    # print(data[0])
    float_list = ['basemean', 'peakmean', 'baseenergymean', 'peakenergymean']
    bool_list = ['sw_parallel']
    int_list = ['base_threads', 'p_id', 'base_copies', 'hw_ncores', 'hw_nchips', 'hw_nthreadspercore']

    sql_ = "INSERT INTO dataspace_%s" % table
    p_float = re.compile('[0-9]*\\.?[0-9]+')
    p_int = re.compile('[0-9]*')
    key_list = []
    item_list = []
    sql_list = []
    for sample in data:
        key_list = []
        item_list = []
        # print(sample["sw_parallel"])
        for key, item in sample.items():
            if key == 'id': continue
            if key in float_list:
                item = item.strip()
                re_res = re.findall(p_float, item)
                if len(re_res) == 0:
                    item = -1
                else:
                    item = float(re_res[0])
            if key in int_list:
                if item == '88i':
                    item = 88

                item = eval(str(item))
                item = int(item)

            if key in bool_list:
                if item == 'Yes':
                    item = True
                else:
                    item = False
            key_list.append(key)
            item_list.append(item)
            print("%s: %s" % (key, item))
        tmp_sql = "INSERT INTO dataspace_%s" % table
        key_sql = '(' + ', '.join(key_list) + ')'

        item_list_tmp = []
        for i in item_list:
            if isinstance(i, bool):
                if i:
                    item_list_tmp.append('TRUE')
                else:
                    item_list_tmp.append('FALSE')

            elif isinstance(i, str):
                item_list_tmp.append("'%s'" % i)

            else:
                item_list_tmp.append(i)

        value_sql = ' VALUES (' + ', '.join(str(i) for i in item_list_tmp) + ')'
        # print('%s%s%s' % (tmp_sql, key_sql, value_sql))
        sql_list.append('%s%s%s' % (tmp_sql, key_sql, value_sql))
    return sql_list


def clean_hard_soft():
    # def clean_hard_soft_data():
    table = 'CINT2017_speeddiv_hard_soft'
    print(table)
    with open(sh_file_path_list[3], 'r') as f:
        data = json.load(f)

    for sample in data:
        sample['p_id'] = sample['id']

    int_list = ["Max_MHz", "Nominal", 'Base_Pointers', 'Peak_Pointers', 'p_id']
    bool_list = ["Parallel"]
    key_dict = {
        "CPU Name": "CPU_name",
        'Max MHz': 'Max_MHz',
        'Max MHz.': 'Max_MHz',
        'Cache L1': 'Cache_L1',
        'L2': 'Cache_L2',
        'L3': 'Cache_L3',
        'File System': 'File_System',
        'System State': 'System_State',
        'Base Pointers': 'Base_Pointers',
        'Peak Pointers': 'Peak_Pointers',
        'Power Management': 'Power_Management',
        'NICs Installed': 'NICs_Installed',
        'Storage Model #s': 'Storage_Model',
        'NICs Connected/Speed': 'NICs_Connected_Speed',
        'Other Storage': 'Other_Storage',
        'Other HW Model #s': 'Other_HW_Model',
        'NICs Enabled (FW/OS)': 'NICs_Enabled_FW_OS',
        'Power Supply': 'Power_Supply',

    }
    sql_ = "INSERT INTO dataspace_%s" % table
    p_float = re.compile('[0-9]*\\.?[0-9]+')
    p_int = re.compile('[0-9]*')
    key_dic = set()
    sql_list = []

    for sample in data:
        key_list = []
        item_list = []

        # print(sample['Storage'])
        # print(sample["sw_parallel"])
        for key, item in sample.items():
            # print(key)
            if key in key_dict:
                key = key_dict[key]
            if key == 'id':
                continue

            if key in int_list:

                try:
                    item = int(item)
                except Exception as e:
                    # print(item)
                    int_re_res = re.findall(p_int, item)
                    item = int(int_re_res[0]) if len(int_re_res[0]) else -1

                assert isinstance(item, int)

            elif key in bool_list:
                if item == 'Yes':
                    item = True
                elif item == 'No':
                    item = False
                assert isinstance(item, bool)
            else:
                # 洗一下
                item = item.replace('\n', ' ')
                item = item.strip()
                # if key == "Compiler":
                #     print(item)

            key_list.append(key)
            item_list.append(item)
            # print("%s: %s" % (key, item))
            # Power_Supply = models.CharField(max_length=128)
            # NICs_Installed = models.CharField(max_length=128)
            # Storage_Model = models.CharField(max_length=128)
            # NICs_Connected_Speed = models.CharField(max_length=128)
            # Other_Storage = models.CharField(max_length=128)
            # Other_HW_Model = models.CharField(max_length=128)
            # NICs_Enabled_FW_OS = models.CharField(max_length=128)
            # Details = models.CharField(max_length=128)
        default_list = [
            'NICs_Connected_Speed', 'Details', "Power_Supply", 'NICs_Installed', 'Storage_Model',
            'NICs_Connected_Speed',
            'Other_Storage', 'Other_HW_Model', 'NICs_Enabled_FW_OS', 'Details', 'Power_Management',
            'CPU_name', 'Max_MHz', 'Nominal', 'Enabled', 'Orderable', 'Cache_L1', 'Cache_L2', 'Cache_L3', 'Other',
            'Memory',
            'Storage', 'OS', 'Compiler', 'Parallel', 'Firmware', 'File_System', 'System_State', 'Base_Pointers',
            'Peak_Pointers', 'Backplane'
        ]
        for default_key in default_list:
            if default_key not in key_list:
                key_list.append(default_key)
                item_list.append("None")

        tmp_sql = "INSERT INTO dataspace_%s" % table
        key_sql = '(' + ', '.join(key_list) + ')'

        item_list_tmp = []
        for i in item_list:
            if isinstance(i, bool):
                if i:
                    item_list_tmp.append('TRUE')
                else:
                    item_list_tmp.append('FALSE')

            elif isinstance(i, str):
                if i == "OS power management: 'cpupower governor is performance', BIOS set to prefer performance at the " \
                        "cost of additional power usage.":
                    i = "OS power management: cpupower governor is performance, BIOS set to prefer performance at the " \
                        "cost of additional power usage."
                item_list_tmp.append("'%s'" % i)

            else:
                item_list_tmp.append(i)

        value_sql = ' VALUES (' + ', '.join(str(i) for i in item_list_tmp) + ')'

        # print('%s%s%s' % (tmp_sql, key_sql, value_sql))
        sql_list.append('%s%s%s' % (tmp_sql, key_sql, value_sql))

table = 'CFP2017_ratediv_result'
print(table)
f_dict = set()

with open('raw_data/data/result/CINT2017_speeddiv_result.json', 'r') as f:
    data = json.load(f)

for sample in data:
    sample['p_id'] = sample['id']

# int_list = ["Max_MHz", "Nominal", 'Base_Pointers', 'Peak_Pointers', 'p_id']
# bool_list = ["Parallel"]


for sample in data:
    if 'SPECrate\u00ae2017_fp_base' in sample.keys():
        continue
    for key, item in sample.items():
        f_dict.add(key)

print(len(f_dict))
print(f_dict)
# {'basecol_time', 'test_sponsor', 'SPECrate2017_fp_base', 'SPECrate2017_fp_peak', 'id', 'peakcol_copies', 'System_Name', 'p_id', 'SPECrate®2017_fp_peak', 'basecol_copies', 'basecol_ratio', 'peakcol_ratio', 'peakcol_time', 'benchmark', 'SPECrate®2017_fp_base'}
# {'peakcol_time', 'id', 'basecol_ratio', 'p_id', 'SPECspeed2017_fp_peak', 'SPECspeed2017_fp_base', 'System_Name', 'test_sponsor', 'SPECspeed®2017_fp_base', 'basecol_threads', 'peakcol_threads', 'SPECspeed®2017_fp_peak', 'benchmark', 'peakcol_ratio', 'basecol_time'}

# print(sql_list)
# 打开数据库连接
db = pymysql.connect(host="localhost", user="root", password="zyx@00223", database="datacenter")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 插入语句  里面的数据类型要对应
sql = "show tables;"

# try:
#     # 执行sql语句
#     for sql in sql_list:
#         print(sql)
#         cursor.execute(sql)
#         # 执行sql语句
#         db.commit()
# except Exception as e:
#     # 发生错误时回滚
#     print(e)
#     print(sql)
#     db.rollback()

# 关闭数据库连接
db.close()
