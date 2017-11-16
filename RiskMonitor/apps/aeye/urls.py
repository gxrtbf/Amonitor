# -*- coding: utf-8 -*-
from django.conf.urls import url

import views

urlpatterns = [
    url(r'^aeyePassRate/$', views.aeyePassRate_view ,name='aeyepassrate'),
    url(r'^aeyeDelayDay/$', views.aeyeDelayDay_view ,name='aeyedelayday'),
    url(r'^aeyeGetRate/$', views.aeyeGetRate_view ,name='aeyegetrate'),
]
