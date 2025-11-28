from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import parsers, filters as rest_filters, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .. import serializers, permissions, filters
from ...core import viewsets, mixins as core_mixins
from ...user.views import restful_apis as user_restful_apis

# Retrieve the user model set in the current Django project
USER_MODEL = get_user_model()



class ClientViewSet(viewsets.ModelViewSet, core_mixins.ActivateModelMixin):
    """
    This class deals with the customers' data, through which you can return all the customers users,
    return the details of a single supervisor, create a supervisor, modify its data, or delete it.

    You must have the permissions in order to perform this operation,
    otherwise you will receive a message stating that you do not have the permissions to perform this event.
    """
    queryset = USER_MODEL.objects.none()
    permission_classes = (permissions.ClientAccessPolicy,)
    serializer_class = serializers.ClientSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    filterset_class = filters.ClientFilter




class ClientProfileViewSet(user_restful_apis.ProfileViewSet):
    """
    A class for dealing with the logged-in user,
    as it contains a set of APIs, such as returning user information, updating user data,
    or deleting the user from the system.
    """
    queryset = USER_MODEL.objects.none()
    permission_classes = (permissions.ProfileAccessPolicy,)
    serializer_class = serializers.ClientSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)

    def update(self, request, *args, **kwargs):
        """
        This method is used to update the profile object.
        We customize this method because we set the partial to true.
        """
        kwargs.setdefault('partial', False)
        return super(ClientProfileViewSet, self).update(request, *args, **kwargs)


