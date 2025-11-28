import django_filters
from ..user import filters


class ClientFilter(filters.UserFilter):
    """
    This class used to filter all clients based some fields and return to viewset model.
    """
    country = django_filters.CharFilter(field_name='client__city__country')

    city = django_filters.CharFilter(field_name='client__city')
