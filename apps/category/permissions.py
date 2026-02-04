from rest_access_policy import AccessPolicy


class CategoryAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": "<safe_methods>",
            "principal": ["authenticated"],
            "effect": "allow",
        },
        {
            "action": ["create", "update", "<method:patch>", "destroy", "active", "disable"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition_expression": ["(admin or editor or supervisor)"]
        }
    ]

    @classmethod
    def scope_queryset(cls, request, queryset):
        user = request.user
        if user.is_anonymous:
            return queryset.model.objects.none()

        # Admin sees everything (including inactive) but not deleted
        if getattr(user, 'is_admin', False):
            return queryset.model.objects.filter(is_deleted=False)

        # Editor / supervisor only see activated (is_active=True) and non-deleted objects
        if getattr(user, 'is_editor', False) or getattr(user, 'is_supervisor', False):
            return queryset.model.activated_objects.filter(is_deleted=False)

        # Other authenticated roles (client) read-only: active and non-deleted only
        return queryset.model.activated_objects.filter(is_deleted=False)
