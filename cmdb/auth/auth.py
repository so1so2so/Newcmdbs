from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from cmdb import models


class LuffyAuth(BaseAuthentication):

    def authenticate(self, request):
        token = request.query_params.get('token')
        obj = models.UserProfile.objects.filter(token=token).first()
        if not obj:
            raise AuthenticationFailed({'code': 1001, 'error': '认证失败'})
        return (obj.user.user, obj)
