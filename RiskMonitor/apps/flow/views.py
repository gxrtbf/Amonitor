# -*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required


@permission_required('part_admin.businessPage')
def flowLoan_view(request):
    return render(request,'flow/flowLoan.html')

@permission_required('part_admin.businessPage')
def flowRepayment_view(request):
    return render(request,'flow/flowRepayment.html')

@permission_required('part_admin.businessPage')
def flowIncome_view(request):
    return render(request,'flow/flowIncome.html')

@permission_required('part_admin.businessPage')
def flowDelayRateFund_view(request):
    return render(request,'flow/flowDelayRateFund.html')

@permission_required('part_admin.businessPage')
def flowLoanFund_view(request):
    return render(request,'flow/flowLoanFund.html')
