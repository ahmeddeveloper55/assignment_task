from functools import wraps


def disable_for_fixture(signal_handler):
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs.get('raw', False):
            return None
        signal_handler(*args, **kwargs)

    return wrapper
