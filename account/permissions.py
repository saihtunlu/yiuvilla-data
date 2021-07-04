def is_allowed_to_create_user(user):
    if user and user.permissions.filter(name='User', create=True) or user.is_superuser:
        return True
    return False


def is_allowed_to_read_user(user):
    if user and user.permissions.filter(name='User', read=True) or user.is_superuser:
        return True
    return False


def is_allowed_to_update_user(user):
    if user and user.permissions.filter(name='User', update=True) or user.is_superuser:
        return True
    return False


def is_allowed_to_delete_user(user):
    if user and user.permissions.filter(name='User', delete=True) or user.is_superuser:
        return True
    return False
