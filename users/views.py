from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.cache import cache
from .models import Profile
# from .utils import get_seven_days_read_data
from .forms import RegForm, LoginFrom

from datacenter.views import home
from dataspace.views import result_list

# Create your views here.

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # school = reg_form.changed_data['school']
            user = User.objects.create_user(username, email, password)  # 创建用户
            company = reg_form.cleaned_data['company']
            # sex = reg_form.cleaned_data['sex']


            user.save()
            profile = Profile.objects.create(user=user, sex=False, company=company)
            profile.save()



            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            user_id = user.id
            cache.set('user_id_%s' % user_id, 0, timeout=1800)

            return render(request, 'index.html', {'massage': '恭喜你已经成功注册啦，赶紧试试吧！'})
    else:
        reg_form = RegForm()
    #
    context = {}
    context['reg_form'] = reg_form
    context['form_title'] = '注册'
    return render(request, 'users/register.html', context)


def login(request):
    if request.method == 'POST':
        login_form = LoginFrom(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)

            context = {'log_massage': request.GET.get('from')}
            context['massage'] = '登陆成功'
            # return redirect(request.GET.get('from', reverse('home')))
            user_id = user.id
            cache.set('user_id_%s' % user_id, 0, timeout=1800)
            return result_list(request, 1, 1)
    else:
        login_form = LoginFrom()
    #
    context = {}
    # context['page_title'] = '欢迎'
    context['login_form'] = login_form
    context['form_title'] = '登录'
    return render(request, 'users/login.html', context)


def logout(request):
    user_id = request.user.id
    cache.delete('user_id_%s' % user_id)
    auth.logout(request)

    return redirect(request.GET.get('from', reverse('home')))
