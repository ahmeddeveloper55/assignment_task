from rest_access_policy import AccessPolicy
from ..user import permissions as user_permissions

class EditorAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": "<safe_methods>",
            "principal": ["anonymous", "authenticated"],
            "effect": "allow",
        },
        {
            "action": "create",
            "principal": ["anonymous", "authenticated"],
            "effect": "allow",
            "condition_expression": ["(admin or anonymous)"]
        },
        {
            "action": ["update", "<method:patch>"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["allow_update_editor"]
        },
        {
            "action": ["active", "disable", "destroy"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["admin"]
        }
    ]

    @classmethod
    def scope_queryset(cls, request, queryset):
        user = request.user

        if user.is_authenticated and user.is_admin:
            return queryset.model.undeleted_objects.all()

        return queryset.model.verified_objects.all()

    def allow_update_editor(self, request, view, action) -> bool:
        user = request.user
        editor = view.get_object()

        if user.is_authenticated and user.is_admin:
            return True

        elif user.is_authenticated and user.is_editor:
            return user.editoruser.editor == editor

        return False


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
        return request.user.editoruser.editor
