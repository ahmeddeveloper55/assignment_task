def zfill(number, repetition=10):
    """
    This function is used to return the char number
    """
    default_number = '0' * (repetition - 1) + '1'

    if not number:
        return default_number

    return str(int(number) + 1).zfill(repetition)


def has_null_value(d):
    """
    If it's a dictionary, check if any value is None recursively; otherwise,
    check if it's None.
    """
    return any(has_null_value(value) for value in d.values()) if isinstance(d, dict) else d is None

