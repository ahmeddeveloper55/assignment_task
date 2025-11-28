from rest_access_policy.access_policy import AccessPolicy
from ..user import permissions as user_permissions


class SupervisorAccessPolicy(AccessPolicy):
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
        user = request.user

        if user.is_authenticated and user.is_admin:
            return queryset.model.undeleted_objects.admins()

        return queryset.model.objects.none()


class ProfileAccessPolicy(user_permissions.ProfileAccessPolicy):
    statements = [
        {
            "action": "*",
            "principal": ["authenticated"],
            "effect": "allow",
            "condition_expression": ["(login_allowed and admin)"]
        }
    ]

    @classmethod
    def scope_object(cls, request, queryset):
        return request.user
