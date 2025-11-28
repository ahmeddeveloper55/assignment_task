from rest_access_policy import AccessPolicy


class CategoryAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": "<safe_methods>",
            "principal": ["authenticated"],
            "effect": "allow",
        },
        {
            "action": ["create", "update", "<method:patch>", "destroy"],
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

        if getattr(user, 'is_admin', False):
            return queryset.model.objects.all()

        # editor + supervisor: only activated categories
        if getattr(user, 'is_editor', False) or getattr(user, 'is_supervisor', False):
            return queryset.model.activated_objects.all()

        # others: only activated
        return queryset.model.activated_objects.all()
