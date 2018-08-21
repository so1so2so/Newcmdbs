# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


# Create your models here.
class Asset(models.Model):
    asset_type_choices = (
        ('server', u'服务器'),
        ('networkdevice', u'网络设备'),
        ('storagedevice', u'存储设备'),
        ('securitydevice', u'安全设备'),
        ('securitydevice', u'机房设备'),
        ('switch', u'交换机'),
        ('router', u'路由器'),
        ('firewall', u'防火墙'),
        ('storage', u'存储设备'),
        ('NLB', u'NetScaler'),
        ('wireless', u'无线AP'),
        ('software', u'软件资产'),
        ('others', u'其它类'),
    )
    asset_type = models.CharField(choices=asset_type_choices, max_length=64, default='server', verbose_name="设备类型")
    name = models.CharField(max_length=64, unique=True)
    sn = models.CharField(u'资产SN号', max_length=128, unique=True)
    # manufactory = models.ForeignKey('Manufactory', verbose_name=u'制造商', null=True, blank=True)
    # model = models.ForeignKey('ProductModel', verbose_name=u'型号')
    # model = models.CharField(u'型号',max_length=128,null=True, blank=True )

    management_ip = models.GenericIPAddressField(u'管理IP', blank=True, null=True)

    # contract = models.ForeignKey('Contract', verbose_name=u'合同', null=True, blank=True)
    trade_date = models.DateField(u'购买时间', null=True, blank=True)
    expire_date = models.DateField(u'过保修期', null=True, blank=True)
    price = models.FloatField(u'价格', null=True, blank=True)
    # business_unit = models.ForeignKey('BusinessUnit', verbose_name=u'所属业务线', null=True, blank=True)
    # tags = models.ManyToManyField('Tag', blank=True)
    # admin = models.ForeignKey('UserProfile', verbose_name=u'资产管理员', null=True, blank=True)
    # idc = models.ForeignKey('IDC', verbose_name=u'IDC机房', null=True, blank=True)

    status_choices = ((0, '在线'),
                      (1, '已下线'),
                      (2, '未知'),
                      (3, '故障'),
                      (4, '备用'),
                      )
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="状态")
    # status = models.ForeignKey('Status', verbose_name = u'设备状态',default=1)
    # Configuration = models.OneToOneField('Configuration',verbose_name='配置管理',blank=True,null=True)

    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = "资产总表"

    def __unicode__(self):
        return self.name


class Server(models.Model):
    """服务器设备"""
    asset = models.OneToOneField('Asset')
    sub_assset_type_choices = (
        (0, 'PC服务器'),
        (1, '刀片机'),
        (2, '小型机'),
    )
    created_by_choices = (
        ('auto', 'Auto'),
        ('manual', 'Manual'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_assset_type_choices, verbose_name="服务器类型", default=0)
    created_by = models.CharField(choices=created_by_choices, max_length=32,
                                  default='auto')  # auto: auto created,   manual:created manually
    hosted_on = models.ForeignKey('self', related_name='hosted_on_server', blank=True, null=True)  # for vitural server
    # sn = models.CharField(u'SN号',max_length=128)
    # management_ip = models.CharField(u'管理IP',max_length=64,blank=True,null=True)
    # manufactory = models.ForeignKey(verbose_name=u'制造商',max_length=128,null=True, blank=True)
    model = models.CharField(verbose_name=u'型号', max_length=128, null=True, blank=True)
    # 若有多个CPU，型号应该都是一致的，故没做ForeignKey

    # nic = models.ManyToManyField('NIC', verbose_name=u'网卡列表')
    # disk
    raid_type = models.CharField(u'raid类型', max_length=512, blank=True, null=True)
    # physical_disk_driver = models.ManyToManyField('Disk', verbose_name=u'硬盘',blank=True,null=True)
    # raid_adaptor = models.ManyToManyField('RaidAdaptor', verbose_name=u'Raid卡',blank=True,null=True)
    # memory
    # ram_capacity = models.IntegerField(u'内存总大小GB',blank=True)
    # ram = models.ManyToManyField('Memory', verbose_name=u'内存配置',blank=True,null=True)

    os_type = models.CharField(u'操作系统类型', max_length=64, blank=True, null=True)
    os_distribution = models.CharField(u'发型版本', max_length=64, blank=True, null=True)
    os_release = models.CharField(u'操作系统版本', max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = '服务器具体信息'
        verbose_name_plural = "服务器具体信息"
        # together = ["sn", "asset"]

    def __unicode__(self):
        return '%s sn:%s' % (self.asset.name, self.asset.sn)


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, telephone, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not telephone:
            raise ValueError('Users must have an telephone ')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            telephone=telephone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password, telephone):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            telephone=telephone,

        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    telephone = models.IntegerField(verbose_name="电话号码")
    name = models.CharField(max_length=64, verbose_name="姓名")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'telephone', ]

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = "用户表"
        permissions = (
            ('crm_table_list', '可以查看kingadmin每张表里所有的数据'),
        )


class Token(models.Model):
    user = models.OneToOneField(to="UserProfile")
    token = models.CharField(max_length=64)
    expre_date = models.DateTimeField(blank=True, auto_now_add=True)