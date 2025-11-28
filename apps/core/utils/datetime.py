from django.utils import timezone
from hijri_converter import Hijri, Gregorian


def now():
    """
    Return an aware or naive datetime.datetime, depending on settings.USE_TZ.
    """
    return timezone.now()


def localtime(value=None):
    """
    Return an aware or naive datetime.datetime, depending on settings.USE_TZ.
    """
    return timezone.localtime(value)


def is_hijri_date(date):
    """
    This function checks the date format,
    if the date is in Hijri format, it returns true, otherwise it returns false.
    """
    try:
        Hijri(date.year, date.month, date.day)._check_date()
        return True
    except OverflowError:
        return False


def to_hijri_format(date):
    """
    This function converts from the Gregorian format to the Hijri format.
    """

    if is_hijri_date(date):
        return date

    return Gregorian(date.year, date.month, date.day).to_hijri()


def to_gregorian_format(date):
    """
    This function converts from the Hijri format to the Gregorian format.
    """

    if not is_hijri_date(date):
        return date

    return Hijri(date.year, date.month, date.day).to_gregorian()
