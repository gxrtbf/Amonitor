# -*- coding: utf-8 -*-
from django.conf.urls import url

import views

urlpatterns = [
    url(r'^marketNum/$', views.marketNum_view ,name='marketNum'),
]
