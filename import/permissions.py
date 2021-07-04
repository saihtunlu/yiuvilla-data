def is_allowed_to_create_imports(user):
    if user and user.permissions.filter(name='Imports', create=True) or user.is_superuser:
        return True
    return False


def is_allowed_to_read_imports(user):
    if user and user.permissions.filter(name='Imports', read=True) or user.is_superuser:
        return True
    return False


def is_allowed_to_update_imports(user):
    if user and user.permissions.filter(name='Imports', update=True) or user.is_superuser:
        return True
    return False


def is_allowed_to_delete_imports(user):
    if user and user.permissions.filter(name='Imports', delete=True) or user.is_superuser:
        return True
    return False
