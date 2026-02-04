from rest_access_policy import AccessPolicy


class ProgramAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": "<safe_methods>",
            "principal": ["authenticated"],
            "effect": "allow",
        },
        # Create / update / activate / deactivate programs: admin, editor, supervisor
        {
            "action": ["create", "update", "<method:patch>", "active", "disable"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition_expression": ["(admin or editor or supervisor)"],
        },
        # Destroy (soft-delete) programs: admin, supervisor only
        {
            "action": ["destroy"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition_expression": ["(admin or supervisor)"],
        },
    ]

    @classmethod
    def scope_queryset(cls, request, queryset):
        user = request.user

        if user.is_anonymous:
            return queryset.model.objects.none()

        # Admin sees everything (including inactive) but not deleted
        if getattr(user, "is_admin", False):
            return queryset.model.objects.filter(is_deleted=False).select_related('category')

        # Editor / supervisor only see activated (is_active=True) and non-deleted objects
        if getattr(user, "is_editor", False) or getattr(user, "is_supervisor", False):
            return queryset.model.activated_objects.filter(is_deleted=False).select_related('category')

        # Other authenticated roles (client) read-only: active, published, and non-deleted only
        return queryset.model.activated_objects.filter(is_deleted=False, is_published=True).select_related('category')


class DiscoveryAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": "<safe_methods>",
            "principal": ["*"],
            "effect": "allow",
        },
    ]   
    @classmethod
    def scope_queryset(cls, request, queryset):
        return queryset.model.objects.filter(is_deleted=False,is_active=True).published().select_related("category")

