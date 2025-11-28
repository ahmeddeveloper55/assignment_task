from rest_access_policy import AccessPolicy


class ProgramAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": "<safe_methods>",
            "principal": ["authenticated"],
            "effect": "allow",
        },
        # Create / update programs: admin, editor, supervisor
        {
            "action": ["create", "update", "<method:patch>"],
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

        # Admin sees everything (including inactive)
        if getattr(user, "is_admin", False):
            return queryset.model.objects.all().select_related('category')

        # Editor / supervisor only see activated objects
        if getattr(user, "is_editor", False) or getattr(user, "is_supervisor", False):
            return queryset.model.activated_objects.all().select_related('category')

        # Other authenticated roles (client if they hit CMS) read-only, active only
        return queryset.model.activated_objects.all().select_related('category')


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
        return queryset.model.objects.published().select_related("category")

