# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from cmdb import models
admin.site.register(models.Asset)
admin.site.register(models.Server)