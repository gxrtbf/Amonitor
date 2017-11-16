# -*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required

@permission_required('part_admin.riskPage')
def aeyePassRate_view(request):
    return render(request,'aeye/aeyePassRate.html')

@permission_required('part_admin.riskPage')
def aeyeDelayDay_view(request):
    return render(request,'aeye/aeyeDelayDay.html')

@permission_required('part_admin.riskPage')
def aeyeGetRate_view(request):
    return render(request,'aeye/aeyeGetRate.html')


