from django import forms
from dal import autocomplete
from django_select2.forms import ModelSelect2Widget
from django.contrib import auth
from dataspace.models import OS
from .os_dict import os_dict


class MLFrom(forms.Form):
    Hz = forms.CharField(label='Max_Hz',
                         widget=forms.TextInput(
                             attrs={'class': 'form-control', 'placeholder': '请输入数值'}))
    cores = forms.CharField(label='cores',
                            widget=forms.TextInput(
                                attrs={'class': 'form-control', 'placeholder': '请输入数值'}))
    Nominal = forms.CharField(label='Nominal',
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'placeholder': '请输入数值'}))
    L1_I = forms.CharField(label='Cache L1_I',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control', 'placeholder': '请输入数值(KB)'}))
    L1_D = forms.CharField(label='Cache L1_D',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control', 'placeholder': '请输入数值(KB)'}))
    L2 = forms.CharField(label='Cache L2',
                         widget=forms.TextInput(
                             attrs={'class': 'form-control', 'placeholder': '请输入数值(KB)'}))
    L3 = forms.CharField(label='Cache L3',
                         widget=forms.TextInput(
                             attrs={'class': 'form-control', 'placeholder': '请输入数值(KB)'}))
    Base_Pointers = forms.CharField(label='Base_Pointers',
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control', 'placeholder': '请输入数值(bit)'}))

    Peak_Pointers = forms.CharField(label='Peak_Pointers',
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control', 'placeholder': '请输入数值(bit)'}))

    Memory = forms.CharField(label='Memory',
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': '请输入数值(GB)'}))

    def clean_hz(self):
        Hz = self.cleaned_data['Hz']
        if Hz == "":
            raise forms.ValidationError("不能为空")
        try:
            Hz = float(Hz)
        except Exception as e:
            raise forms.ValidationError("必须是数值")

        if Hz < 0:
            raise forms.ValidationError("必须是正整数")
        return Hz

    def clean_cores(self):
        Hz = self.cleaned_data['cores']
        if Hz == "":
            raise forms.ValidationError("不能为空")
        try:
            Hz = float(Hz)
        except Exception as e:
            raise forms.ValidationError("必须是数值")

        if Hz < 0:
            raise forms.ValidationError("必须是正整数")
        return Hz

    def clean_Nominal(self):
        Hz = self.cleaned_data['Nominal']
        if Hz == "":
            raise forms.ValidationError("不能为空")
        try:
            Hz = float(Hz)
        except Exception as e:
            raise forms.ValidationError("必须是数值")

        if Hz < 0:
            raise forms.ValidationError("必须是正整数")
        return Hz

    def clean_L1_I(self):
        Hz = self.cleaned_data['L1_I']
        if Hz == "":
            raise forms.ValidationError("不能为空")
        try:
            Hz = float(Hz)
        except Exception as e:
            raise forms.ValidationError("必须是数值")

        if Hz < 0:
            raise forms.ValidationError("必须是正整数")
        return Hz

    def clean_L1_D(self):
        L1_D = self.cleaned_data['L1_D']
        if L1_D == "":
            raise forms.ValidationError("不能为空")
        try:
            L1_D = float(L1_D)
        except Exception as e:
            raise forms.ValidationError("必须是数值")

        if L1_D < 0:
            raise forms.ValidationError("必须是正整数")
        return L1_D

    def clean_L2(self):
        Hz = self.cleaned_data['L2']
        if Hz == "":
            raise forms.ValidationError("不能为空")
        try:
            Hz = float(Hz)
        except Exception as e:
            raise forms.ValidationError("必须是数值")

        if Hz < 0:
            raise forms.ValidationError("必须是正整数")
        return Hz

    def clean_L3(self):
        Hz = self.cleaned_data['L3']
        if Hz == "":
            raise forms.ValidationError("不能为空")
        try:
            Hz = float(Hz)
        except Exception as e:
            raise forms.ValidationError("必须是数值")

        if Hz < 0:
            raise forms.ValidationError("必须是正整数")
        return Hz

    def clean_Base_Pointers(self):
        Hz = self.cleaned_data['Base_Pointers']
        if Hz == "":
            raise forms.ValidationError("不能为空")
        try:
            Hz = float(Hz)
        except Exception as e:
            raise forms.ValidationError("必须是数值")

        if Hz < 0:
            raise forms.ValidationError("必须是正整数")
        return Hz

    def clean_Peak_Pointers(self):
        Hz = self.cleaned_data['Peak_Pointers']
        if Hz == "":
            raise forms.ValidationError("不能为空")
        try:
            Hz = float(Hz)
        except Exception as e:
            raise forms.ValidationError("必须是数值")

        if Hz < 0:
            raise forms.ValidationError("必须是正整数")
        return Hz

    def clean_Memory(self):
        Hz = self.cleaned_data['Memory']
        if Hz == "":
            raise forms.ValidationError("不能为空")
        try:
            Hz = float(Hz)
        except Exception as e:
            raise forms.ValidationError("必须是数值")

        if Hz < 0:
            raise forms.ValidationError("必须是正整数")
        return Hz

    # def clean(self):
    #     Hz = self.cleaned_data['Hz']
    #     cores = self.cleaned_data['cores']
    #
    #     if user is None:
    #         raise forms.ValidationError('用户名或密码错误')
    #     else:
    #         self.cleaned_data['user'] = user
    #
    #     return self.cleaned_data
