from django.urls import path
from . import views

urlpatterns = [
    # path('save_result/', views.save_CFP2017_ratediv_result, name='save_result'),
    # path('save_result/', views.save_result, name='login'),
    # path('save_benchmark/', views.save_benchmark, name='save_benchmark'),
    # path('logout/', views.logout, name='logout'),
    path('result_list/<int:table_number>/<int:page_number>/', views.result_list, name='result_list'),
    path('details/<int:table_number>/<int:p_id>/', views.details, name='details'),
    path('search/<str:keywords>/<int:page_number>', views.search, name='search'),
    path('hs_su/', views.hs_su, name='hs_su'),
    path('data_create/', views.data_create, name='data_create'),
    path('train_SVM/', views.train_SVM, name='train_SVM'),
    path('train_tree/', views.train_tree, name='train_tree'),
    path('summary_hard_soft_improve/', views.summary_hard_soft_improve, name='summary_hard_soft_improve'),


]