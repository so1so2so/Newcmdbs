#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from django.conf.urls import url,include
from cmdb import views
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'GetAsset', views.GetAsset)
router.register(r'GetServer', views.GetServer)


urlpatterns = [
    url(r'^(?P<version>[v1|v2]+)/', include(router.urls)),
 ]




# urlpatterns = [
#     url(r'^(?P<version>[v1|v2]+)/GetAsset/$', views.GetAsset.as_view({'get': 'list','post':'create'}),name='GetAsset'),
#     url(r'^(?P<version>[v1|v2]+)/GetAsset/(?P<pk>\d+)/$', views.GetAsset.as_view({'get': 'retrieve','delete':'destroy','put':'update','patch':'partial_update'}),name="GetAsset_up"),
#
#      url(r'^(?P<version>[v1|v2]+)/GetServer/$', views.GetServer.as_view({'get': 'list','post':'create'}),name='GetServer'),
#     url(r'^(?P<version>[v1|v2]+)/GetServer/(?P<pk>\d+)/$', views.GetServer.as_view({'get': 'retrieve','delete':'destroy','put':'update','patch':'partial_update'}),name="GetServer_up"),
#
#
# ]
