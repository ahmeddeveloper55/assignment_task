from rest_access_policy.access_policy import AccessPolicy


class EpisodeAccessPolicy(AccessPolicy):
    """
    CMS access to episodes.
    """
    statements = [
        {
            "action": "<safe_methods>",
            "principal": ["authenticated"],
            "effect": "allow",
        },
        {
            "action": ["create", "update", "<method:patch>", "active", "disable"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition_expression": ["(admin or editor or supervisor)"],
        },
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
        if getattr(user, 'is_admin', False):
            return queryset.model.objects.filter(is_deleted=False).select_related('program', 'program__category')

        # Editor / supervisor only see activated (is_active=True) and non-deleted objects
        if getattr(user, 'is_editor', False) or getattr(user, 'is_supervisor', False):
            return queryset.model.activated_objects.filter(is_deleted=False).select_related('program', 'program__category')

        # Other authenticated roles (client) read-only: active, published, and non-deleted only
        return queryset.model.activated_objects.filter(is_deleted=False, is_published=True).select_related('program', 'program__category')


class DiscoveryEpisodeAccessPolicy(AccessPolicy):
    """
    Discovery access to episodes.
    """
    statements = [
        {
            "action": "<safe_methods>",
            "principal": ["*"],
            "effect": "allow",
        },
    ]

    @classmethod
    def scope_queryset(cls, request, queryset):
        return queryset.model.objects.filter(is_deleted=False,is_active=True).published().select_related('program', 'program__category')
