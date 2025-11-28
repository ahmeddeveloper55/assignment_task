import typing
from urllib.parse import urlparse

from aliyunsdkcore.http.http_request import HttpRequest
from django.conf import settings
from rest_access_policy.access_policy import AccessPolicy
from rest_framework_api_key.permissions import HasAPIKey as DefaultHasAPIKey


class SafeAccountAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["<safe_methods>"],
            "principal": "anonymous",
            "effect": "allow",

        }
    ]

    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:
        user = request.user

        if user.is_authenticated and user.is_admin:
            return fields

        fields.pop('is_deleted', None)
        fields.pop('deleted_at', None)
        fields.pop('sort_order', None)
        return fields


