# -*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User as authuser
from django import forms
from .models import User

class UserForm(forms.Form):
    email = forms.CharField(label='邮箱',max_length=20)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())

def login_view(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            email = uf.cleaned_data['email']
            password = uf.cleaned_data['password']
            user = User.objects.filter(email=email, password=password)
            if user:
                user = authenticate(username=email, password=password)
                if user is not None and user.is_active:
                    login(request,user)
                return HttpResponseRedirect("/index/") 
            else:
                return render(request,'login/login.html',{'sign': '账号或密码输入错误！'})
        else:
            return render(request,'login/login.html',{'sign': '输入无效！'})
    else:
        uf = UserForm()
    	return render(request,'login/login.html')

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login/") 


