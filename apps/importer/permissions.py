# apps/importer/permissions.py
from rest_framework.permissions import BasePermission


class ImportAccessPermission(BasePermission):
    """
    Only admin / supervisor / editor can use importer endpoints.
    Clients must not import content.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        return (
            getattr(user, "is_admin", False)
            or getattr(user, "is_supervisor", False)
            or getattr(user, "is_editor", False)
        )