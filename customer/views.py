from .models import Customer
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .serializers import CustomerSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .permissions import is_allowed_to_create_customer, is_allowed_to_read_customer, is_allowed_to_update_customer, is_allowed_to_delete_customer
from app.pagination import Pagination

# Create your views here.


class Customers(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializers
    pagination_class = Pagination

    def get_queryset(self):
        return Customer.objects.all().order_by('-created_at')

    def get(self, request):
        if is_allowed_to_read_customer(request.user):
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


class SearchCustomer(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if is_allowed_to_read_customer(request.user):
            customers = Customer.objects.filter(
                name__icontains=request.GET['query']).order_by('-created_at')
            customer_serializer = CustomerSerializers(customers, many=True)
            return Response(customer_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('You are not allowed!', status=status.HTTP_401_UNAUTHORIZED)


class SingleCustomer(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if is_allowed_to_create_customer(request.user):
            data = request.data['data']
            customer = Customer()
            customer_serializer = CustomerSerializers(customer, data=data)
            if customer_serializer.is_valid():
                customer_serializer.save()
                return Response(customer_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('You are not allowed!', status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        if is_allowed_to_update_customer(request.user):
            data = request.data['data']
            id = request.GET['customer_id']
            customer = get_object_or_404(
                Customer, id=id)
            customer_serializer = CustomerSerializers(customer, data=data)
            if customer_serializer.is_valid():
                customer_serializer.save()
                return Response(customer_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('You are not allowed!', status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, **kwargs):
        id = request.GET['customer_id']
        customer = get_object_or_404(
            Customer, id=id)
        customer_serializer = CustomerSerializers(customer, many=False)
        return Response(customer_serializer.data, status=status.HTTP_200_OK)


class RemoveMultiCustomers(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if is_allowed_to_delete_customer(request.user):
            data = request.data['data']
            Customer.objects.filter(pk__in=data).delete()
            return Response('Success', status=status.HTTP_200_OK)
        else:
            return Response('You are not allowed!', status=status.HTTP_401_UNAUTHORIZED)
