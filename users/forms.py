from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile


class LoginFrom(forms.Form):
    username = forms.CharField(label='用户名',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误')
        else:
            self.cleaned_data['user'] = user

        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=30, min_length=2,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': '请输入3至30位用户名'}))

    company = forms.CharField(label='公司名',
                              max_length=30, min_length=2,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))
    SEX = [
        ['男', '男'],
        ['女', '女']
    ]
    sex = forms.ChoiceField(label='性别', choices=SEX)

    password = forms.CharField(label='密码',
                               min_length=6,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    password_again = forms.CharField(label='再次输入密码',
                                     min_length=6,
                                     widget=forms.PasswordInput(
                                         attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已存在")
        return username

    def clean_sex(self):
        sex = self.cleaned_data['sex']
        return sex

    def clean_company(self):
        company = self.cleaned_data['company']
        return company

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已被使用")
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError("两次密码不一致")
        return password_again
