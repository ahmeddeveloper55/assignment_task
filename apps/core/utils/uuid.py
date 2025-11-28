from uuid import UUID


def is_valid_uuid(uuid):
    try:
        return bool(UUID(uuid))
    except (TypeError, ValueError, AttributeError):
        return False
