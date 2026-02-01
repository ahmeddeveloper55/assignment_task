from rest_access_policy.access_policy import AccessPolicy


class TagAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": "<safe_methods>",
            "principal": ["authenticated"],
            "effect": "allow",
        },
        {
            "action": ["create", "update", "<method:patch>", "active", "disable", "destroy"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition_expression": ["(admin or editor or supervisor)"],
        }
    ]

    @classmethod
    def scope_queryset(cls, request, queryset):
        user = request.user

        if user.is_anonymous:
            return queryset.model.objects.none()

        if getattr(user, "is_admin", False):
            return queryset.model.objects.all()
        
        # Editor / supervisor only see activated objects
        if getattr(user, "is_editor", False) or getattr(user, "is_supervisor", False):
            return queryset.model.activated_objects.all()
        
        


        return queryset.model.activated_objects.all()

    @classmethod
    def scope_fields(cls, request, fields: dict, instance=None) -> dict:
        user = request.user

        if user.is_authenticated and user.is_admin:
            return fields

        fields.pop('created_at', None)
        fields.pop('updated_at', None)
        fields.pop('is_active', None)
        fields.pop('enabled_at', None)
        fields.pop('note', None)
        fields.pop('created_by', None)
        fields.pop('updated_by', None)
        return fields
