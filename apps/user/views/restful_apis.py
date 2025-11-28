from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, parsers, filters as rest_filters
from rest_framework.response import Response
from rest_framework.decorators import action

from ...core import get_timezone_choices, viewsets, mixins as core_mixins
from .. import serializers, permissions, filters, GenderChoices, RoleChoices

"""
 ============================================================== 
     Django RESTfull API (application programming interface)
 ============================================================== 
"""

UserModel = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This class deals with the users' data, through which you can return all the users,
    return the details of a single user.

    You must have the permissions in order to perform this operation,
    otherwise you will receive a message stating that you do not have the permissions to perform this event.
    """
    queryset = UserModel.objects.none()
    permission_classes = (permissions.UserAccessPolicy,)
    serializer_class = serializers.UserSerializer
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    filterset_class = filters.UserFilter
    search_fields = filters.UserSearchFields

    @action(methods=['get'], detail=False)
    def roles(self, request, *args, **kwargs):
        """
        This API is used to return the roles of users like admins, vendors
        or shops
        """
        return Response(RoleChoices.choices)

    @action(methods=['get'], detail=False)
    def genders(self, request, *args, **kwargs):
        """
        This function is used to return genders of user profile
        """
        return Response(GenderChoices.choices)

    @action(methods=['get'], detail=False)
    def timezones(self, request, *args, **kwargs):
        """
        This function is used to return list of timezones
        """
        return Response(get_timezone_choices())


class ProfileViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    A class for dealing with the logged-in user,
    as it contains a set of APIs, such as returning user information, updating user data,
    or deleting the user from the system.
    """
    queryset = UserModel.objects.none()
    permission_classes = (permissions.ProfileAccessPolicy,)
    serializer_class = serializers.UserSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)

    def get_object(self):
        """
        This function is used to return the value of a specified object by
        either the object number or the token associated with the object
        """
        return self.access_policy.scope_object(self.request, self.queryset)

    def list(self, request, *args, **kwargs):
        """
        This API returns the logged-in user's data, such as his email, phone number,
        username, last login date, and others.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        This method is used to update the profile object.
        We customize this method because we set the partial to true.
        """
        kwargs.setdefault('partial', True)
        return super(ProfileViewSet, self).update(request, *args, **kwargs)
