from rest_access_policy.access_policy import AccessPolicy
from ..user import permissions as user_permissions


class IndexAccessPolicy(AccessPolicy):
    """Define a class for controlling access to index views."""

    """
    Define statements for access control.
    Each statement specifies the action, principal, effect, and condition expression.
    """
    statements = [
        {
            "action": "*",
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["admin"]
        }
    ]

    @classmethod
    def scope_queryset(cls, request, queryset):
        """
        Limit the queryset based on user permissions.

        @param request: The request object.
        @param queryset: The queryset to be filtered.
        @return: A filtered queryset based on user permissions.
        """
        user = request.user

        if user.is_authenticated and user.is_admin:
            return queryset.model.undeleted_objects.clients()

        return queryset.model.objects.none()


class ClientAccessPolicy(AccessPolicy):
    """Define a class for controlling access to client views."""

    """
    Define statements for access control.
    Each statement specifies the action, principal, effect, and condition expression.
    """
    statements = [
        {
            "action": "*",
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["admin"]
        }
    ]

    @classmethod
    def scope_queryset(cls, request, queryset):
        """
        Limit the queryset based on user permissions.

        @param request: The request object.
        @param queryset: The queryset to be filtered.
        @return: A filtered queryset based on user permissions.
        """
        user = request.user

        if user.is_authenticated and user.is_admin:
            return queryset.model.undeleted_objects.clients()

        return queryset.model.objects.none()


class ProfileAccessPolicy(user_permissions.ProfileAccessPolicy):
    """Define a class for controlling access to user views."""

    """
    Define statements for access control.
    Each statement specifies the action, principal, effect, and condition expression.
    """
    statements = [
        {
            "action": "*",
            "principal": ["authenticated"],
            "effect": "allow",
            "condition_expression": ["(login_allowed and client)"]
        }
    ]

    @classmethod
    def scope_object(cls, request, queryset):
        """
        Set the object scope to the provider of the current user.

        @param request: The request object.
        @param queryset: The queryset to be filtered (unused in this method).
        @return: The provider of the current user as the object scope.
        """
        return request.user
