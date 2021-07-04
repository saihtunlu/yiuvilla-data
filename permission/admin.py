from django.contrib import admin
from .models import RolePermission, Role,  UserPermission
models = [RolePermission, Role,  UserPermission]
# Register your models here.
admin.site.register(models)
