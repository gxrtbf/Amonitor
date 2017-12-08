# -*- coding: utf-8 -*-
from django.conf.urls import url

import views

urlpatterns = [
    url(r'^userIncrease/$', views.userIncrease_view ,name='increase'),
    url(r'^userSex/$', views.userInfoSex_view ,name='sex'),
    url(r'^userAge/$', views.userInfoAge_view ,name='age'),
    url(r'^userRest/$', views.userRest_view ,name='rest'),
    url(r'^userRestAll/$', views.userRestAll_view ,name='restall'),
    url(r'^userLocation/$', views.userInfoLocation_view ,name='location'),
]
