#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from rest_framework import serializers
from cmdb import models


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        fields = "__all__"
        dept = 2


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Server
        fields = "__all__"
        # depth  = 2

