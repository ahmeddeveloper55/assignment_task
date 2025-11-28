from ..core import managers as core_managers
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class ClientsQueryset(core_managers.BaseQuerySet):
    """
    Represent a lazy database lookup for a set of objects.
    """


class BaseClientManager(core_managers.BaseManager):
    def get_queryset(self):
        return ClientsQueryset(self.model, using=self._db)

    def get_or_create_by_phone(self, phone):
        """
        `phone` is a normalized PhoneNumber (same validator as your client API).
        - If a User with this phone exists, use it.
        - Else create one via create_client(phone_number=...), which:
            * assigns role=Client,
            * generates a username (utils.generate_username),
            * sets password behaviour identical to your Client API.
        Then ensure a Client row exists for that User.
        """
        with transaction.atomic():
            user = User.objects.find_by_phone_number(phone).first()
            if not user:
                user = User.objects.create_create_client(phone_number=phone)
            client, _ = self.get_or_create(user=user)
            return client


