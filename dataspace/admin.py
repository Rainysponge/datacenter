from django.contrib import admin
from .models import *


# Register your models here.


@admin.register(CFP2017_ratediv)
class CFP2017_ratediv_Admin(admin.ModelAdmin):
    list_display = ('p_id', 'test_sponsor', 'System_Name', 'basemean', 'peakmean')


@admin.register(CFP2017_speeddiv)
class CFP2017_speeddiv_Admin(admin.ModelAdmin):
    list_display = ('p_id', 'test_sponsor', 'System_Name', 'basemean', 'peakmean')


@admin.register(CINT2017_ratediv)
class CINT2017_ratediv_Admin(admin.ModelAdmin):
    list_display = ('p_id', 'test_sponsor', 'System_Name', 'basemean', 'peakmean')


@admin.register(CINT2017_speeddiv)
class CINT2017_speeddiv_Admin(admin.ModelAdmin):
    list_display = ('p_id', 'test_sponsor', 'System_Name', 'basemean', 'peakmean')


@admin.register(CINT2017_speeddiv_hard_soft)
class CINT2017_speeddiv_hard_soft_Admin(admin.ModelAdmin):
    list_display = ('p_id', 'CPU_name', 'Max_MHz', 'Cache_L1')


@admin.register(CINT2017_ratediv_hard_soft)
class CINT2017_ratediv_hard_soft_Admin(admin.ModelAdmin):
    list_display = ('p_id', 'CPU_name', 'Max_MHz', 'Cache_L1')


@admin.register(CFP2017_ratediv_hard_soft)
class CFP2017_ratediv_hard_soft_Admin(admin.ModelAdmin):
    list_display = ('p_id', 'CPU_name', 'Max_MHz', 'Cache_L1')


@admin.register(CFP2017_speeddiv_hard_soft)
class CINT2017_speeddiv_hard_soft_Admin(admin.ModelAdmin):
    list_display = ('p_id', 'CPU_name', 'Max_MHz', 'Cache_L1')


# Benchmark
@admin.register(Benchmark)
class Benchmark_Admin(admin.ModelAdmin):
    list_display = ('pk', 'benchmark_name',)


@admin.register(CFP2017_ratediv_result)
class CFP2017_ratediv_result_Admin(admin.ModelAdmin):
    list_display = ('p_id', 'test_sponsor', 'System_Name', 'turn', 'benchmark')


@admin.register(SPECrate2017_ratediv_fp_score)
class SPECrate2017_ratediv_fp_score_Admin(admin.ModelAdmin):
    list_display = ('p_id', 'test_sponsor', 'System_Name', 'SPECrate2017_fp_base', 'SPECrate2017_fp_peak')


# SPECrate2017_result/

# SPECrate2017_ratediv_int_score
@admin.register(SPECrate2017_ratediv_int_score)
class SPECrate2017_ratediv_int_score_Admin(admin.ModelAdmin):
    list_display = ('p_id', 'test_sponsor', 'System_Name', 'SPECrate2017_int_base', 'SPECrate2017_int_peak')


@admin.register(CINT2017_ratediv_result)
class CINT2017_ratediv_result_Admin(admin.ModelAdmin):
    list_display = ('p_id', 'test_sponsor', 'System_Name', 'turn', 'benchmark')


@admin.register(OS)
class OS_Admin(admin.ModelAdmin):
    list_display = ('id', 'OS_name', 'OS_value')

