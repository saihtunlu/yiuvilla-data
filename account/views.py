from .models import User
from permission.models import UserPermission, Role
from permission.serializers import UserPermissionSerializers
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from app.pagination import Pagination
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import is_allowed_to_read_user
# Create your views here.


class Staffs(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = Pagination

    def get_queryset(self):
        query = self.request.GET['query']
        queryset = User.objects.filter(is_staff=True, is_superuser=False, username__icontains=query).exclude(
            role="Owner").order_by('-date_joined')
        return queryset

    def get(self, request):
        if is_allowed_to_read_user(request.user):
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
        else:
            return Response('You are not allowed!', status=status.HTTP_401_UNAUTHORIZED)


class SingleStaff(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if "staff_id" in request.GET:
            id = request.GET["staff_id"]
            staff = User.objects.get(
                is_superuser=False, is_staff=True, pk=id)
            user_serializer = UserSerializer(staff, many=False)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        else:
            staffs = User.objects.filter(
                is_superuser=False, is_staff=True)
            user_serializer = UserSerializer(staffs, many=True)
            return Response(user_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        data = request.data
        permissions = data['permissions']
        staffs = User.objects.get(id=data['id'])
        user_serializer = UserSerializer(staffs, data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            UserPermission.objects.filter(user=staffs).delete()
            for data2 in permissions:
                permission = UserPermission(user=staffs)  # add foreign key
                permission_serializer = UserPermissionSerializers(
                    permission, data=data2)
                if permission_serializer.is_valid():
                    permission_serializer.save()
                else:
                    return Response(permission_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Auth(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        data = request.data['data']
        permissions = data['permissions']
        user = User.objects.get(id=data['id'])
        user_serializer = UserSerializer(user, data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            UserPermission.objects.filter(user=user).delete()
            for data2 in permissions:
                permission = UserPermission(user=user)  # add foreign key
                permission_serializer = UserPermissionSerializers(
                    permission, data=data2)
                if permission_serializer.is_valid():
                    permission_serializer.save()
                else:
                    return Response(permission_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user_serializer = UserSerializer(request.user, many=False)
        return Response(user_serializer.data, status=status.HTTP_200_OK)


class Users(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        staffs = User.objects.filter(is_superuser=False)
        user_serializer = UserSerializer(staffs, many=True)
        return Response(user_serializer.data, status=status.HTTP_200_OK)


class ToggleActivateUsers(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        id = kwargs['id']
        user = User.objects.get(id=id)
        user.is_active = not user.is_active
        user.save()
        return Response('Success', status=status.HTTP_201_CREATED)


class Login(APIView):
    def post(self, request):
        user_email = request.data['email']
        user_password = request.data['password']

        try:
            user = User.objects.get(email=user_email)
            if not user.check_password(user_password):
                return Response({'detail': 'The password you entered is not correct!'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                token = RefreshToken.for_user(
                    user
                )  # generate token without username & password
                response = {}
                response["access"] = str(token.access_token)
                response["refresh"] = str(token)
                return Response(response, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'detail': 'There is no user with email you entered!'}, status=status.HTTP_404_NOT_FOUND)
