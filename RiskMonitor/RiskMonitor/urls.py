"""RiskMonitor URL Configuration"""
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^', include('apps.login.urls')),
    url(r'^', include('apps.index.urls')),
    url(r'^', include('apps.userInfo.urls')),
    url(r'^', include('apps.flow.urls')),
    url(r'^', include('apps.finance.urls')),
    url(r'^', include('apps.aeye.urls')),
    url(r'^', include('apps.market.urls')),
    url(r'^', include('apps.collect.urls')),

    url(r'^', include('api.dayAddApi.urls')),
    url(r'^', include('api.actualApi.urls')),
]
