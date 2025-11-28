from django.utils.translation import gettext_lazy


def _(str: str):
    """
    Turn any callable into a lazy evaluated callable. result classes or types
    is required -- at least one is needed so that the automatic forcing of
    the lazy evaluation code is triggered. Results are not memoized; the
    function is evaluated on every access.
    """
    return gettext_lazy(str)
