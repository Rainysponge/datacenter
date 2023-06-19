from django.db import models


# Create your models here.


class CFP2017_ratediv(models.Model):
    # major = models.CharField(max_length=10) {'base_copies', 'Config', 'System_Name', 'PDF', 'hw_ncores', 'id',
    # 'HTML', 'peakenergymean', 'CSV', 'test_sponsor', 'hw_nchips', 'hw_nthreadspercore', 'baseenergymean', 'PS',
    # 'peakmean', 'Text', 'basemean'}
    p_id = models.IntegerField(unique=True)
    test_sponsor = models.CharField(max_length=128)
    System_Name = models.CharField(max_length=128)
    HTML = models.CharField(max_length=128)
    CSV = models.CharField(max_length=128)
    Text = models.CharField(max_length=128)
    PDF = models.CharField(max_length=128)
    PS = models.CharField(max_length=128)
    Config = models.CharField(max_length=128)
    base_copies = models.IntegerField()
    hw_ncores = models.IntegerField()
    hw_nchips = models.IntegerField()
    hw_nthreadspercore = models.IntegerField()
    basemean = models.FloatField()
    peakmean = models.FloatField()
    baseenergymean = models.FloatField()
    peakenergymean = models.FloatField()

    def __str__(self):
        return "test_sponsor: %s, System_Name: %s" % (self.test_sponsor, self.System_Name)


class CFP2017_speeddiv(models.Model):
    p_id = models.IntegerField(unique=True)
    test_sponsor = models.CharField(max_length=128)
    System_Name = models.CharField(max_length=128)
    HTML = models.CharField(max_length=128)
    CSV = models.CharField(max_length=128)
    Text = models.CharField(max_length=128)
    PDF = models.CharField(max_length=128)
    PS = models.CharField(max_length=128)
    Config = models.CharField(max_length=128)
    # base_copies = models.IntegerField()
    sw_parallel = models.BooleanField()
    hw_ncores = models.IntegerField()
    hw_nchips = models.IntegerField()
    hw_nthreadspercore = models.IntegerField()
    basemean = models.FloatField()
    peakmean = models.FloatField()
    base_threads = models.IntegerField()
    baseenergymean = models.FloatField()
    peakenergymean = models.FloatField()

    def __str__(self):
        return "test_sponsor: %s, System_Name: %s" % (self.test_sponsor, self.System_Name)


class CINT2017_ratediv(models.Model):
    p_id = models.IntegerField(unique=True)
    test_sponsor = models.CharField(max_length=128)
    System_Name = models.CharField(max_length=128)
    HTML = models.CharField(max_length=128)
    CSV = models.CharField(max_length=128)
    Text = models.CharField(max_length=128)
    Config = models.CharField(max_length=128)
    PDF = models.CharField(max_length=128)
    PS = models.CharField(max_length=128)
    base_copies = models.IntegerField()
    hw_ncores = models.IntegerField()
    hw_nchips = models.IntegerField()
    hw_nthreadspercore = models.IntegerField()
    basemean = models.FloatField()
    peakmean = models.FloatField()
    baseenergymean = models.FloatField()
    peakenergymean = models.FloatField()

    def __str__(self):
        return "test_sponsor: %s, System_Name: %s" % (self.test_sponsor, self.System_Name)


class CINT2017_speeddiv(models.Model):
    p_id = models.IntegerField(unique=True)
    test_sponsor = models.CharField(max_length=128)
    System_Name = models.CharField(max_length=128)
    HTML = models.CharField(max_length=128)
    CSV = models.CharField(max_length=128)
    Text = models.CharField(max_length=128)
    Config = models.CharField(max_length=128)
    PDF = models.CharField(max_length=128)
    PS = models.CharField(max_length=128)
    sw_parallel = models.BooleanField()
    # base_copies = models.IntegerField()/
    hw_ncores = models.IntegerField()
    hw_nchips = models.IntegerField()
    hw_nthreadspercore = models.IntegerField()
    basemean = models.FloatField()
    peakmean = models.FloatField()
    baseenergymean = models.FloatField()
    base_threads = models.IntegerField()
    peakenergymean = models.FloatField()

    def __str__(self):
        return "test_sponsor: %s, System_Name: %s" % (self.test_sponsor, self.System_Name)


# {'System State', 'Power Supply', 'NICs Enabled (FW/OS)', 'CPU Name', 'OS', 'p_id', 'L2', 'Peak Pointers', 'Details',
# 'Other', 'Storage Model #s', 'Enabled', 'Other HW Model #s', 'Cache L1', 'Max MHz.', 'Orderable', 'Nominal', 'Max MHz'
# , 'id', 'Other Storage', 'NICs Connected/Speed', 'L3', 'Parallel', 'Storage', 'Power Management', 'Compiler',
# 'NICs Installed', 'Backplane', 'File System', 'Memory', 'Base Pointers', 'Firmware'}

class CFP2017_speeddiv_hard_soft(models.Model):
    p_id = models.IntegerField(unique=True)
    CPU_name = models.CharField(max_length=128)
    Max_MHz = models.IntegerField()
    Nominal = models.IntegerField()
    Enabled = models.CharField(max_length=128)
    Orderable = models.CharField(max_length=128)
    Cache_L1 = models.CharField(max_length=128)
    Cache_L2 = models.CharField(max_length=128)
    Cache_L3 = models.CharField(max_length=128)
    Other = models.CharField(max_length=512)
    Memory = models.CharField(max_length=128)
    Storage = models.CharField(max_length=512)
    OS = models.CharField(max_length=128)
    Compiler = models.CharField(max_length=256)
    Parallel = models.BooleanField()
    Firmware = models.CharField(max_length=128)
    File_System = models.CharField(max_length=128)
    System_State = models.CharField(max_length=128)

    Base_Pointers = models.IntegerField()
    Peak_Pointers = models.IntegerField()
    Power_Management = models.CharField(max_length=128)
    Power_Supply = models.CharField(max_length=128)
    NICs_Installed = models.CharField(max_length=128)
    Storage_Model = models.CharField(max_length=128)
    NICs_Connected_Speed = models.CharField(max_length=128)
    Other_Storage = models.CharField(max_length=128)
    Other_HW_Model = models.CharField(max_length=128)
    NICs_Enabled_FW_OS = models.CharField(max_length=128)
    Details = models.CharField(max_length=128)
    Backplane = models.CharField(max_length=128)


class CFP2017_ratediv_hard_soft(models.Model):
    p_id = models.IntegerField(unique=True)
    CPU_name = models.CharField(max_length=128)
    Max_MHz = models.IntegerField()
    Nominal = models.IntegerField()
    Enabled = models.CharField(max_length=128)
    Orderable = models.CharField(max_length=128)
    Cache_L1 = models.CharField(max_length=128)
    Cache_L2 = models.CharField(max_length=128)
    Cache_L3 = models.CharField(max_length=128)
    Other = models.CharField(max_length=512)
    Memory = models.CharField(max_length=128)
    Storage = models.CharField(max_length=256)
    OS = models.CharField(max_length=128)
    Compiler = models.CharField(max_length=256)
    Parallel = models.BooleanField()
    Firmware = models.CharField(max_length=128)
    File_System = models.CharField(max_length=128)
    System_State = models.CharField(max_length=128)
    Base_Pointers = models.IntegerField()
    Peak_Pointers = models.IntegerField()
    Power_Management = models.CharField(max_length=128)

    Power_Supply = models.CharField(max_length=128)
    NICs_Installed = models.CharField(max_length=128)
    Storage_Model = models.CharField(max_length=128)
    NICs_Connected_Speed = models.CharField(max_length=128)
    Other_Storage = models.CharField(max_length=128)
    Other_HW_Model = models.CharField(max_length=128)
    NICs_Enabled_FW_OS = models.CharField(max_length=128)
    Details = models.CharField(max_length=128)
    Backplane = models.CharField(max_length=128)


class CINT2017_ratediv_hard_soft(models.Model):
    p_id = models.IntegerField(unique=True)
    CPU_name = models.CharField(max_length=128)
    Max_MHz = models.IntegerField()
    Nominal = models.IntegerField()
    Enabled = models.CharField(max_length=128)
    Orderable = models.CharField(max_length=128)
    Cache_L1 = models.CharField(max_length=128)
    Cache_L2 = models.CharField(max_length=128)
    Cache_L3 = models.CharField(max_length=128)
    Other = models.CharField(max_length=512)
    Memory = models.CharField(max_length=128)
    Storage = models.CharField(max_length=256)
    OS = models.CharField(max_length=128)
    Compiler = models.CharField(max_length=256)
    Parallel = models.BooleanField()
    Firmware = models.CharField(max_length=128)
    File_System = models.CharField(max_length=128)
    System_State = models.CharField(max_length=128)
    Base_Pointers = models.IntegerField()
    Peak_Pointers = models.IntegerField()
    Power_Management = models.CharField(max_length=128)

    Power_Supply = models.CharField(max_length=128)
    NICs_Installed = models.CharField(max_length=128)
    Storage_Model = models.CharField(max_length=128)
    NICs_Connected_Speed = models.CharField(max_length=128)
    Other_Storage = models.CharField(max_length=128)
    Other_HW_Model = models.CharField(max_length=128)
    NICs_Enabled_FW_OS = models.CharField(max_length=128)
    Details = models.CharField(max_length=128)
    Backplane = models.CharField(max_length=128)


class CINT2017_speeddiv_hard_soft(models.Model):
    p_id = models.IntegerField(unique=True)
    CPU_name = models.CharField(max_length=128)
    Max_MHz = models.IntegerField()
    Nominal = models.IntegerField()
    Enabled = models.CharField(max_length=128)
    Orderable = models.CharField(max_length=128)
    Cache_L1 = models.CharField(max_length=128)
    Cache_L2 = models.CharField(max_length=128)
    # Cache_L2 = models.CharField(max_length=128)
    Cache_L3 = models.CharField(max_length=128)
    Other = models.CharField(max_length=512)
    Memory = models.CharField(max_length=128)
    Storage = models.CharField(max_length=256)
    OS = models.CharField(max_length=128)
    Compiler = models.CharField(max_length=256)
    Parallel = models.BooleanField()
    Firmware = models.CharField(max_length=128)
    File_System = models.CharField(max_length=128)
    System_State = models.CharField(max_length=128)
    Base_Pointers = models.IntegerField()
    Peak_Pointers = models.IntegerField()
    Power_Management = models.CharField(max_length=128)

    Power_Supply = models.CharField(max_length=128)
    NICs_Installed = models.CharField(max_length=128)
    Storage_Model = models.CharField(max_length=128)
    NICs_Connected_Speed = models.CharField(max_length=128)
    Other_Storage = models.CharField(max_length=128)
    Other_HW_Model = models.CharField(max_length=128)
    NICs_Enabled_FW_OS = models.CharField(max_length=128)
    Details = models.CharField(max_length=128)
    Backplane = models.CharField(max_length=128)


#     {'System_Name', 'SPECrate®2017_fp_base', 'SPECrate®2017_fp_peak', 'test_sponsor', 'id', 'p_id'}
# class CFP2017_speeddiv__benchmark_result(models.Model):
#     p_id = models.IntegerField()
#     test_sponsor = models.CharField(max_length=128)
#     System_Name = models.CharField(max_length=128)
#     # basecol_time = models.CharField()
# # {'basecol_time', 'System_Name', 'test_sponsor', 'id', 'basecol_ratio', 'p_id', 'peakcol_ratio', 'basecol_copies',
# # 'benchmark', 'peakcol_time', 'peakcol_copies'}
# {'basecol_time', 'id', 'test_sponsor', 'SPECrate2017_fp_base', 'p_id', 'benchmark', 'peakcol_ratio', 'SPECrate2017_fp_peak', 'peakcol_time', 'System_Name', 'basecol_ratio', 'basecol_copies', 'peakcol_copies'}

class Benchmark(models.Model):
    benchmark_name = models.CharField(max_length=64)


# raw_data/data/result/CFP2017_ratediv_result.json
class CFP2017_ratediv_result(models.Model):
    p_id = models.IntegerField()
    test_sponsor = models.CharField(max_length=128)
    System_Name = models.CharField(max_length=128)
    benchmark = models.ForeignKey(Benchmark, on_delete=models.CASCADE)

    turn = models.IntegerField()
    basecol_time = models.FloatField()
    # SPECrate2017_fp_base = models.FloatField()
    # SPECrate2017_fp_peak = models.FloatField()
    peakcol_time = models.FloatField()
    basecol_ratio = models.FloatField()
    peakcol_ratio = models.FloatField()
    basecol_copies = models.FloatField()
    peakcol_copies = models.FloatField()


# SPECrate2017_fp_base
class SPECrate2017_ratediv_fp_score(models.Model):
    p_id = models.IntegerField()
    test_sponsor = models.CharField(max_length=128)
    System_Name = models.CharField(max_length=128)

    SPECrate2017_fp_base = models.FloatField()
    SPECrate2017_fp_peak = models.FloatField()


class CINT2017_ratediv_result(models.Model):
    p_id = models.IntegerField()
    test_sponsor = models.CharField(max_length=128)
    System_Name = models.CharField(max_length=128)
    benchmark = models.ForeignKey(Benchmark, on_delete=models.CASCADE)

    turn = models.IntegerField()
    basecol_time = models.FloatField()
    # SPECrate2017_fp_base = models.FloatField()
    # SPECrate2017_fp_peak = models.FloatField()
    peakcol_time = models.FloatField()
    basecol_ratio = models.FloatField()
    peakcol_ratio = models.FloatField()
    basecol_copies = models.FloatField()
    peakcol_copies = models.FloatField()


class SPECrate2017_ratediv_int_score(models.Model):
    p_id = models.IntegerField()
    test_sponsor = models.CharField(max_length=128)
    System_Name = models.CharField(max_length=128)

    SPECrate2017_int_peak = models.FloatField()
    SPECrate2017_int_base = models.FloatField()


# {'basecol_time',  'basecol_ratio', 'peakcol_time', 'peakcol_ratio', 'System_Name', 'id', 'benchmark',
# 'basecol_threads', 'p_id', 'peakcol_threads', 'test_sponsor', }
class CFP2017_speeddiv_result(models.Model):
    p_id = models.IntegerField()
    test_sponsor = models.CharField(max_length=128)
    System_Name = models.CharField(max_length=128)
    benchmark = models.ForeignKey(Benchmark, on_delete=models.CASCADE)

    turn = models.IntegerField()
    basecol_time = models.FloatField()

    peakcol_time = models.FloatField()
    basecol_ratio = models.FloatField()
    peakcol_ratio = models.FloatField()
    basecol_threads = models.FloatField()
    peakcol_threads = models.FloatField()

class SPECrate2017_speeddiv_fp_score(models.Model):
    p_id = models.IntegerField()
    test_sponsor = models.CharField(max_length=128)
    System_Name = models.CharField(max_length=128)

    SPECrate2017_fp_base = models.FloatField()
    SPECrate2017_fp_peak = models.FloatField()

class CINT2017_speeddiv_result(models.Model):
    p_id = models.IntegerField()
    test_sponsor = models.CharField(max_length=128)
    System_Name = models.CharField(max_length=128)
    benchmark = models.ForeignKey(Benchmark, on_delete=models.CASCADE)

    turn = models.IntegerField()
    basecol_time = models.FloatField()

    peakcol_time = models.FloatField()
    basecol_ratio = models.FloatField()
    peakcol_ratio = models.FloatField()
    basecol_threads = models.FloatField()
    peakcol_threads = models.FloatField()

class SPECrate2017_speeddiv_int_score(models.Model):
    p_id = models.IntegerField()
    test_sponsor = models.CharField(max_length=128)
    System_Name = models.CharField(max_length=128)

    SPECrate2017_int_base = models.FloatField()
    SPECrate2017_int_peak = models.FloatField()

class summary_results_company(models.Model):
    task_number = models.IntegerField()
    company_name = models.CharField(max_length=128)
    base_score = models.FloatField()
    peak_score = models.FloatField()

class summary_results_Hz(models.Model):
    task_number = models.IntegerField()
    hz = models.FloatField()
    base_score = models.FloatField()
    peak_score = models.FloatField()


class sponsor_system(models.Model):
    sponsor = models.CharField(max_length=128)
    System_name = models.CharField(max_length=128)



class OS(models.Model):
    OS_name = models.CharField(max_length=128)
    OS_value = models.IntegerField()
    task_number = models.IntegerField()
    base = models.FloatField()
    peak = models.FloatField()

class improve_peak_base(models.Model):
    test_sponsor = models.CharField(max_length=128)
    improve_score = models.FloatField()
    task = models.IntegerField()

