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
    asset = serializers.CharField(source='asset.name')
    sub_asset_type=serializers.CharField(source='get_sub_asset_type_display')
    class Meta:
        model = models.Server
        # fields = "__all__"
        fields = ['asset', 'id', 'created_by', 'model', 'raid_type', 'os_type','sub_asset_type']
        depth = 0
