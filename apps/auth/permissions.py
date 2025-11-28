from rest_access_policy.access_policy import AccessPolicy


class LoginAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": "*",
            "principal": ["anonymous"],
            "effect": "allow"
        }
    ]

class RestPasswordAccessPolicy(AccessPolicy):
    """
    Define access guideline for login views.
    Inherits from user_permissions.ProfileAccessPolicy.
    """

    statements = [
        {
            "action": "*",
            "principal": ["anonymous"],
            "effect": "allow"
        }
    ]
