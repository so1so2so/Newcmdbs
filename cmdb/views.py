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

from api.api2.Runner import ANSRunner
import os

BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
yaml_path = os.path.join(BASE_DIR, 'playbook')


# from ansible.errors import AnsibleError


# from api.api2.Runner import ANSRunner

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


class ansible_ad_host(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html", )

    def post(self, request, *args, **kwargs):
        resource = []
        results = request.data.dict()
        for k, v in results.items():
            if v == "":
                results.pop(k)
        if results.get("hostname"):
            pass
        elif results.get("ip"):
            results['hostname'] = results.get("ip")
        else:
            # print "必须有hostname,或者IP地址"
            return render(request, "index.html", {"result": "必须填写IP,HOSTNAME"})
        # print results
        resource.append(results)
        rbt = ANSRunner(resource)
        rbt.run_model(host_list=['default_group'], module_name='setup', module_args="filter=*")
        result = rbt.get_model_result()
        import json
        result = json.loads(result)
        print result
        ip = results.get("ip")
        hostvisiable = ip.replace('.', '_')
        resultss = result['success'][hostvisiable]['ansible_facts']
        return render(request, "index.html", {"result": resultss})


class ansible_playbook(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "playbook.html")

    def post(self, request, *args, **kwargs):
        yaml_path_file = os.path.join(yaml_path, 'service_check')
        return render(request, "playbook.html")
