from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import parsers, filters as rest_filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ...core import viewsets, mixins as core_mixins
from ...user.views import restful_apis as user_restful_apis
from ...auth import jwt_response
from .. import models, permissions, serializers, filters
class EditorViewSet(core_mixins.CachedViewSetMixin, viewsets.ModelViewSet, core_mixins.ActivateModelMixin):
    """
    This class deals with the owner data, through which you can return all the owners,
    return the details of a single owner, create an owner, modify its data, or delete it.

    You must have the permissions in order to perform this operation,
    otherwise you will receive a message stating that you do not have the permissions to perform this event.
    """
    permission_classes = (permissions.EditorAccessPolicy,)
    queryset = models.Editor.objects.none()
    serializer_class = serializers.EditorSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    filterset_class = filters.EditorFilter
    search_fields = filters.EditorSearchFields
    cache_timeout = 60 * 15

    def get_jwt_response(self, user):
        """
        Returns the response data for both the login and refresh views.
        Override to return a custom response such as including the
        serialized representation of the User.
        @return: user payload
        """
        return jwt_response.jwt_response_payload_handler(user, request=self.request)

    def perform_create(self, serializer):
        kwargs = {'created_by': self.request.user if self.request.user.is_authenticated else None}
        return serializer.save(**kwargs)

    def get_response(self, owner, serializer):
        """
        This method is used to return the response when created owner.
        :return: response
        """
        user = self.request.user

        if user.is_authenticated and user.is_admin:
            return serializer.data

        return self.get_jwt_response(owner.manager())

    def create(self, request, *args, **kwargs):
        """
        Create a new instance of EDITOR.

        This method handles incoming POST requests to create a new instance
        of EDITOR based on the data provided in the request. The serialized
        data from the request is passed to the serializer's create method,
        which performs the actual instance creation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        owner = self.perform_create(serializer)
        response = self.get_response(owner=owner, serializer=serializer)
        return Response(response, status=status.HTTP_201_CREATED)


class EditorProfileViewSet(user_restful_apis.ProfileViewSet):
    """
    A class for dealing with the logged-in user,
    as it contains a set of APIs, such as returning user information, updating user data,
    or deleting the user from the system.
    """
    queryset = models.Editor.objects.none()
    permission_classes = (permissions.ProfileAccessPolicy,)
    serializer_class = serializers.EditorSerializer
