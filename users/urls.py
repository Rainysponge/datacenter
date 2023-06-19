from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    # path('changeProfileInfo/<int:profile_pk>', views.changeProfileInfo, name='changeProfileInfo'),
    # path('changeTSInfo/<int:profile_pk>', views.changeTSInfo, name='changeTSInfo'),
    # path('changeTS_student_Info/<int:profile_pk>', views.changeTS_student_Info, name='changeTS_student_Info'),

    # path('teacher/', views.teacher_info, name='teacher_info'),


]