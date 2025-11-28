from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import parsers, filters as rest_filters

from ...core import viewsets, mixins as core_mixins
from ...user.views import restful_apis as user_restful_apis
from .. import serializers, permissions, filters

"""
 ============================================================== 
     Django RESTfull API (application programming interface)
 ============================================================== 
"""

USER_MODEL = get_user_model()


class SupervisorViewSet(viewsets.ModelViewSet, core_mixins.ActivateModelMixin):
    """
    This class deals with the admins' data, through which you can return all the admins users,
    return the details of a single supervisor, create a supervisor, modify its data, or delete it.

    You must have the permissions in order to perform this operation,
    otherwise you will receive a message stating that you do not have the permissions to perform this event.
    """

    queryset = USER_MODEL.objects.none()
    permission_classes = (permissions.SupervisorAccessPolicy,)
    serializer_class = serializers.SupervisorSerialize
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    filterset_class = filters.SupervisorFilter


class SupervisorProfileViewSet(user_restful_apis.ProfileViewSet):
    """
    A class for dealing with the logged-in user,
    as it contains a set of APIs, such as returning user information, updating user data,
    or deleting the user from the system.
    """

    queryset = USER_MODEL.objects.none()
    permission_classes = (permissions.ProfileAccessPolicy,)
    serializer_class = serializers.SupervisorSerialize
