# -*- coding: utf-8 -*-
from django.conf.urls import url

import views

urlpatterns = [
    url(r'^collectRate/$', views.collectRate_view ,name='collectRate'),
    url(r'^collectNum/$', views.collectNum_view ,name='collectNum'),
]
