from rest_access_policy import AccessPolicy



class UserAccessPolicy(AccessPolicy):
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

        if user.is_authenticated and user.is_admin:
            return queryset.model.verified_objects.all()

        elif user.is_authenticated and user.is_editor:
            editor = user.editoruser.editor
            return queryset.model.verified_objects.editors(editoruser__editor=editor)

        elif user.is_authenticated and user.is_client:
            return queryset.model.verified_objects.clients(pk=user.pk)

        return queryset.model.objects.none()


class ProfileAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": "*",
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["login_allowed"]
        }
    ]

    @classmethod
    def scope_object(cls, request, queryset):
        return request.user
