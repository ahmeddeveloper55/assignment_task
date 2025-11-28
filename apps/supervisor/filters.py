from ..user import filters


class SupervisorFilter(filters.UserFilter):
    """
    This class used to filter all admins based some fields and return to viewset model.
    """
