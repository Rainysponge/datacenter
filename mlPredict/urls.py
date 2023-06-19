from django.urls import path

from . import views

urlpatterns = [
    path('predict_SVM/<int:task_number>/<int:model_number>/', views.predict_SVM, name='predict_SVM'),

    path('predict_tree/', views.predict_tree, name='predict_tree'),


]