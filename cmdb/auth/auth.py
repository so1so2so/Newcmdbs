#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from cmdb import models


class Auth(BaseAuthentication):

    def authenticate(self, request):
        token = request.query_params.get('token')
        obj = models.Token.objects.filter(token=token).first()
        if not obj:
            raise AuthenticationFailed({'code': 1001, 'error': '认证失败'})
        return (obj.user.user, obj)
