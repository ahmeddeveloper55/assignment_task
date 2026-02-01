from rest_access_policy import AccessPolicy
from ..user import permissions as user_permissions

class EditorAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": "*",
            "principal": ["authenticated"],
            "effect": "allow",
            "condition_expression": ["(admin or editor)"]
        }
    ]

    @classmethod
    def scope_queryset(cls, request, queryset):
        user = request.user

        if user.is_authenticated and (user.is_admin or user.is_editor):
            return queryset.model.objects.editors()

        return queryset.model.objects.none()


class ProfileAccessPolicy(user_permissions.ProfileAccessPolicy):
    statements = [
        {
            "action": "*",
            "principal": ["authenticated"],
            "effect": "allow",
            "condition_expression": ["(login_allowed and editor)"]
        }
    ]

    @classmethod
    def scope_object(cls, request, queryset):
        return request.user