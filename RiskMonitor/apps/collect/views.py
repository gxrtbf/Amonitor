# -*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

@permission_required('part_admin.collectPage')
def collectRate_view(request):
    return render(request,'collect/collectRate.html')

@permission_required('part_admin.collectPage')
def collectNum_view(request):
    return render(request,'collect/collectNum.html')
