# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from django.views.generic.base import View
from django.shortcuts import render, HttpResponse
from cmdb import models
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.contrib import auth
from cmdb.serial import AssetSerializer
from cmdb.serial import ServerSerializer
from cmdb.base_ret_class.base import Ret_class
import uuid
from cmdb.auth.auth import Auth


class GetAsset(ModelViewSet):
    queryset = models.Asset.objects.all()
    serializer_class = AssetSerializer
    pagination_class = PageNumberPagination


class GetServer(ModelViewSet):
    authentication_classes = [Auth, ]
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
        print request.session.session_key
        return HttpResponse("ok")

    def post(self, request, *args, **kwargs):
        d = Ret_class()
        token = uuid.uuid4().hex
        username = request.data['username']
        pwd = request.data['password']
        print username, pwd
        # 如何判断用户名和密码对不对
        user = auth.authenticate(username=username, password=pwd)
        print user
        if user:
            models.Token.objects.update_or_create(user=user, defaults={'token': token})
            # ret = user.is_authenticated()
            auth.login(request, user)
            d.code = 200
            d.message = '登录成功'
            d.token = token
            return Response(d.__dict__)
        else:
            d.code = 404
            d.message = '登录失败,请检查用户名密码'
            d.token = None
            return Response(d.__dict__)
