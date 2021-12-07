import copy
import datetime

from django.conf import settings
from django.urls import resolve
from django.utils.translation import (
    gettext_lazy as _,
    activate
)
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions

from apps.users.models import User


class BaseTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'
    model = User

    def authenticate(self, request):

        # We escape authentication for swagger urls
        extempted_urls = ['schema-swagger-ui', 'schema-json']
        if resolve(request.path_info).url_name in extempted_urls:
            return (None, None)

        return super().authenticate(request)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            user = model.objects.get(user_id=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        return (user, key)
