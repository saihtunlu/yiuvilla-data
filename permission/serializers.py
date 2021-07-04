from rest_framework import serializers
from .models import Role, RolePermission, UserPermission


class PermissionSerializers(serializers.ModelSerializer):

    class Meta:
        model = RolePermission
        fields = ['id', 'name', 'create', 'update', 'delete', 'read']


class UserPermissionSerializers(serializers.ModelSerializer):

    class Meta:
        model = UserPermission
        fields = ['id', 'name', 'create', 'update', 'delete', 'read','edit_create', 'edit_update', 'edit_delete', 'edit_read']


class RoleSerializers(serializers.ModelSerializer):
    permissions = PermissionSerializers(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ['id',  'name',  'permissions']
