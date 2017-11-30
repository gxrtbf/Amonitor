# -*- coding: utf-8 -*-
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

import views

urlpatterns = [
    url(r'^api/v1/day/$', views.indexhead_item),
]

urlpatterns = format_suffix_patterns(urlpatterns)