from rest_access_policy import AccessPolicy


class SearchAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": "<safe_methods>",
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": ["client"],
        },
    ]

    @staticmethod
    def client(request, view, action) -> bool:
        user = request.user
        return getattr(user, "role", None) == "client"