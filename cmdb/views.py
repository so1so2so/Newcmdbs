# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from django.shortcuts import render, HttpResponse
from cmdb import models
import json
from serial import AssetSerializer
from serial import ServerSerializer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from cmdb.serial import ServerSerializer
from rest_framework.pagination import PageNumberPagination


class GetAsset(ModelViewSet):
    queryset = models.Asset.objects.all()
    serializer_class = AssetSerializer
    pagination_class = PageNumberPagination


class GetServer(ModelViewSet):
    queryset = models.Server.objects.all()
    serializer_class = ServerSerializer
    pagination_class = PageNumberPagination

class Index(APIView):
    def get(self, request, *args, **kwargs):
        # return render(request, '/static/index.html')
        return HttpResponse("ok")
