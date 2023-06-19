from functools import wraps
from django.shortcuts import redirect, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.cache import cache


def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user_id = request.user.id
        if user_id:

            user_info = cache.get('user_id_%s' % user_id)
            if user_info is not None:
                # 用户已登录，执行原函数
                return func(request, *args, **kwargs)
            else:
                # 用户未登录

                auth.logout(request)
                return redirect(reverse('login'))  # 这个地方需要传一个form
        else:
            # 用户未认证或用户ID不存在
            return redirect(reverse('login'))
    return wrapper


