from rest_framework import viewsets

from .mixins import ImportMixin, ExportMixin


class GenericViewSet(viewsets.GenericViewSet):
    """
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    """
    is_public_access_enabled = False
    permission_classes = []

    def get_query_params(self):
        """
        This method is used to return the query params data like params in url.
        """
        return self.request.query_params.dict()

    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable,
        and may be a queryset. Defaults to using `self.queryset`.
        """
        return self.access_policy.scope_queryset(self.request, self.queryset)

    def get_permissions(self):
        """
        Instantiate and return all required permissions for this view.

        Ensures every request must include a valid API key,
        in addition to any view-specific permissions.
        """
        # Instantiate all declared permission classes
        permissions = [perm() for perm in self.permission_classes]



        return permissions


class ReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet, GenericViewSet):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    """
    pass


class ModelViewSet(viewsets.ModelViewSet, GenericViewSet, ImportMixin, ExportMixin):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    def perform_create(self, serializer):
        """
        This method is used to add user that created object.
        """
        data = {}

        if hasattr(self.queryset.model, 'created_by'):
            data.update({'created_by': self.request.user})

        serializer.save(**data)

    def perform_update(self, serializer):
        """
        This method is used to add user that update object.
        """
        data = {}

        if hasattr(self.queryset.model, 'updated_by'):
            data.update({'updated_by': self.request.user})

        serializer.save(**data)
