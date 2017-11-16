# -*- coding: utf-8 -*-
from django.conf.urls import url

import views

urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
]
