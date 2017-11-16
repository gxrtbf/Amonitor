# -*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

@permission_required('part_admin.userPage')
def userIncrease_view(request):
    return render(request,'userInfo/userIncrease.html')

@permission_required('part_admin.userPage')
def userInfoSex_view(request):
    return render(request,'userInfo/userSex.html')

@permission_required('part_admin.userPage')
def userInfoAge_view(request):
    return render(request,'userInfo/userAge.html')

@permission_required('part_admin.userPage')
def userInfoLocation_view(request):
    return render(request,'userInfo/userLocation.html')