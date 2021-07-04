from .models import User
from rest_framework import serializers
from permission.serializers import UserPermissionSerializers


class UserSerializer(serializers.ModelSerializer):

    permissions = UserPermissionSerializers(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'is_superuser', 'first_name',
                  'last_name', 'email', 'avatar', 'username', 'role', 'is_staff', 'is_active', 'last_login', 'phone', 'date_joined', 'permissions']
