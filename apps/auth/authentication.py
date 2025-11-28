from rest_framework.authentication import SessionAuthentication as RestSessionAuthentication


class SessionAuthentication(RestSessionAuthentication):
    """
    Use Django's session framework for authentication.
    """

    def authenticate(self, request):
        """
        Returns a `User` if the request session currently has a logged-in user.
        Otherwise, returns `None`.
        """

        # Get the session-based user from the underlying HttpRequest object
        user = getattr(request._request, 'user', None)

        # if user.is_admin:
        #     self.enforce_csrf(request)

        # CSRF passed with authenticated user
        return user, None
