# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from django.views import View
from django.shortcuts import render, HttpResponse
from cmdb import models
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.contrib import auth
from cmdb.serial import AssetSerializer
from cmdb.serial import ServerSerializer


class GetAsset(ModelViewSet):
    queryset = models.Asset.objects.all()
    serializer_class = AssetSerializer
    pagination_class = PageNumberPagination


class GetServer(ModelViewSet):
    queryset = models.Server.objects.all()
    serializer_class = ServerSerializer
    pagination_class = PageNumberPagination


class Register(APIView):
    def get(self, request, *args, **kwargs):
        # return render(request, '/static/index.html')
        return HttpResponse("ok")


class Login(APIView):

    def get(self, request, *args, **kwargs):
        # return render(request, '/static/index.html')
        return HttpResponse("ok")

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        pwd = request.data['password']
        print username,pwd
        # 如何判断用户名和密码对不对
        user = auth.authenticate(username=username, password=pwd)
        if user:
            # ret = user.is_authenticated()
            auth.login(request, user)
            return HttpResponse("登录成功")
        else:
            print "登录失败"
            return HttpResponse("登录失败,请检查用户名密码")
