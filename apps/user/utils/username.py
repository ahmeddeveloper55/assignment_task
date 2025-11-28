from django.contrib.auth import get_user_model
from random_username import generate


def generate_username():
    """
    This function generates a random token that is used as a unique identifier for the user.
    This code is verified by querying it against the user database.

    If this symbol exists, another symbol is generated other than that,
    and this symbol is approved
    """

    user_model = get_user_model()
    username = generate.generate_username()[0]
    username = user_model.normalize_username(username)

    if not user_model.objects.find_by_username(username).exists():
        return username

    return generate_username()