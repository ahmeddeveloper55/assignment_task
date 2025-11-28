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
            "action": ["create", "update", "<method:patch>"],
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

        if getattr(user, 'is_admin', False):
            return queryset.model.objects.select_related('program', 'program__category')

        if getattr(user, 'is_editor', False) or getattr(user, 'is_supervisor', False):
            return queryset.model.activated_objects.select_related('program', 'program__category')

        # Other authenticated roles: only active episodes
        return queryset.model.activated_objects.select_related('program', 'program__category')


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
        return queryset.model.objects.published().select_related('program', 'program__category')
