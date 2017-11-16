# -*- coding: utf-8 -*-
from django.conf.urls import url

import views

urlpatterns = [
    url(r'^financetodayloan/$', views.finance_view ,name='financetodayloan'),
]
