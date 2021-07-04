from .models import Role,  RolePermission, UserPermission
from account.models import User
from account.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics, pagination
from rest_framework.response import Response
from .serializers import RoleSerializers,  PermissionSerializers, UserPermissionSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from app.pagination import Pagination
# Create your views here.

# Roles


class SearchRole(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Role.objects.filter(
            name__icontains=request.GET['query']).order_by('-created_at')
        role_serializer = RoleSerializers(roles, many=True)
        return Response(role_serializer.data, status=status.HTTP_200_OK)


class Roles(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoleSerializers
    pagination_class = Pagination

    def get_queryset(self):

        if 'query' in self.request.GET:
            query = self.request.GET['query']
            queryset = Role.objects.filter(
                name__icontains=query).order_by('-created_at')
        else:
            queryset = Role.objects.all().order_by('-created_at')
        return queryset

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data  # pagination data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class SingleRole(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data['data']
        permissions = data['permissions']
        role = Role()
        role_serializer = RoleSerializers(role, data=data)
        if role_serializer.is_valid():
            role_serializer.save()
            for permissionData in permissions:
                permission = RolePermission(role=role)  # add foreign key
                permission_serializer = PermissionSerializers(
                    permission, data=permissionData)
                if permission_serializer.is_valid():
                    permission_serializer.save()
            return Response(role_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(role_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data['data']
        permissions = data['permissions']
        role = get_object_or_404(
            Role, id=data['id'])
        role_serializer = RoleSerializers(role, data=data)
        if role_serializer.is_valid():
            role_serializer.save()
            RolePermission.objects.filter(role=role).delete()
            for permissionData in permissions:
                permission = RolePermission(role=role)  # add foreign key
                permission_serializer = PermissionSerializers(
                    permission, data=permissionData)
                if permission_serializer.is_valid():
                    permission_serializer.save()
            users = User.objects.filter(role=role.name)
            print(users)
            for user in users:
                UserPermission.objects.filter(user=user).delete()
                for data in permissions:
                    permission = UserPermission(user=user)  # add foreign key
                    permission_serializer = UserPermissionSerializers(
                        permission, data=data)
                    if permission_serializer.is_valid():
                        permission_serializer.save()
                    else:
                        return Response(permission_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(role_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(role_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        role = get_object_or_404(
            Role, id=id)
        role_serializer = RoleSerializers(role, many=False)
        return Response(role_serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        id = kwargs['id']
        role = get_object_or_404(
            Role, id=id)
        role.delete()
        return Response('Success', status=status.HTTP_201_CREATED)

# UserRoles


class RolePermissions(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = RolePermission.objects.order_by('created_at').reverse()
    serializer_class = PermissionSerializers
    pagination_class = pagination.PageNumberPagination


class SingleRolePermission(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        role = Role.objects.get(id=request.data['role_id'])
        permission = RolePermission(role=role)  # add foreign key
        permission_serializer = PermissionSerializers(permission, data=data)
        if permission_serializer.is_valid():
            permission_serializer.save()
            return Response(permission_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(permission_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data
        permission = get_object_or_404(
            RolePermission, id=request.data['id'])
        permission_serializer = PermissionSerializers(permission, data=data)
        if permission_serializer.is_valid():
            permission_serializer.save()
            return Response(permission_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(permission_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        permission = get_object_or_404(
            RolePermission, id=id)
        permission_serializer = PermissionSerializers(permission, many=False)
        return Response(permission_serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        id = kwargs['id']
        permission = get_object_or_404(
            RolePermission, id=id)
        permission.delete()
        return Response('Success', status=status.HTTP_201_CREATED)


class UserPermissions(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        mainData = request.data
        user = User.objects.get(id=request.data['user_id'])
        for data in mainData['permissions']:
            permission = UserPermission(user=user)  # add foreign key
            permission_serializer = UserPermissionSerializers(
                permission, data=data)
            if permission_serializer.is_valid():
                permission_serializer.save()
            else:
                return Response(permission_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_serializer = UserSerializer(user, many=False)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        mainData = request.data
        user = User.objects.get(id=request.data['user_id'])
        UserPermission.objects.filter(user=user).delete()
        for data in mainData['permissions']:
            permission = UserPermission(user=user)  # add foreign key
            permission_serializer = UserPermissionSerializers(
                permission, data=data)
            if permission_serializer.is_valid():
                permission_serializer.save()
            else:
                return Response(permission_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Success", status=status.HTTP_201_CREATED)
