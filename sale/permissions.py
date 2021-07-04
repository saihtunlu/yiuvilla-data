def is_allowed_to_create_sale(user):
    if user and user.permissions.filter(name='Sale', create=True) or user.is_superuser:
        return True
    return False


def is_allowed_to_read_sale(user):
    if user and user.permissions.filter(name='Sale', read=True) or user.is_superuser:
        return True
    return False


def is_allowed_to_update_sale(user):
    if user and user.permissions.filter(name='Sale', update=True) or user.is_superuser:
        return True
    return False


def is_allowed_to_delete_sale(user):
    if user and user.permissions.filter(name='Sale', delete=True) or user.is_superuser:
        return True
    return False
