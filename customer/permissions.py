def is_allowed_to_create_customer(user):
    if user and user.permissions.filter(name='Customer', create=True) or user.is_superuser:
        return True
    return False


def is_allowed_to_read_customer(user):
    if user and user.permissions.filter(name='Customer', read=True) or user.is_superuser:
        return True
    return False


def is_allowed_to_update_customer(user):
    if user and user.permissions.filter(name='Customer', update=True) or user.is_superuser:
        return True
    return False


def is_allowed_to_delete_customer(user):
    if user and user.permissions.filter(name='Customer', delete=True) or user.is_superuser:
        return True
    return False
