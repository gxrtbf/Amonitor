# -*- coding: utf-8 -*-
from django.conf.urls import url

import views

urlpatterns = [
    url(r'^flowLoan/$', views.flowLoan_view ,name='loan'),
    url(r'^flowRepayment/$', views.flowRepayment_view ,name='repayment'),
    url(r'^flowIncome/$', views.flowIncome_view ,name='income'),
    url(r'^flowDelayRateFund/$', views.flowDelayRateFund_view ,name='delayRateFund'),
    url(r'^flowLoanFund/$', views.flowLoanFund_view ,name='loanFund'),
]
