from customer.models import Customer
from .models import Sale, SaleProduct, SalePayment
from .serializers import SaleProductSerializers, SaleSerializers, SaleListSerializers, SalePaymentSerializers, SaleExportSerializers
from rest_framework import status
from rest_framework import generics
from app.pagination import Pagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .permissions import is_allowed_to_read_sale, is_allowed_to_update_sale, is_allowed_to_delete_sale
from django.db.models.functions import TruncDate
from django.db.models import Count, Sum, Avg
from django.db.models import Q

from django.template.loader import render_to_string
from django.http import HttpResponse


class Sales(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SaleListSerializers
    pagination_class = Pagination

    def get_queryset(self):
        query = self.request.GET['query']
        payment_status = self.request.GET['payment_status']
        is_fullfilled_params = self.request.GET['is_fullfilled']
        date = self.request.GET['date']

        if is_fullfilled_params == 'true':
            is_fullfilled = True
            queryset = Sale.objects.filter(
                Q(
                    sale_no__icontains=query, date__icontains=date, is_fullfilled=is_fullfilled,  payment_status__icontains=payment_status) | Q(
                    customer__name__icontains=query, date__icontains=date, is_fullfilled=is_fullfilled,  payment_status__icontains=payment_status)).order_by('-updated_at')
            return queryset
        elif is_fullfilled_params == 'false':
            is_fullfilled = False
            queryset = Sale.objects.filter(
                Q(
                    sale_no__icontains=query, date__icontains=date, is_fullfilled=is_fullfilled,  payment_status__icontains=payment_status) | Q(
                    customer__name__icontains=query, date__icontains=date, is_fullfilled=is_fullfilled,  payment_status__icontains=payment_status)).order_by('-updated_at')
            return queryset
        else:
            queryset = Sale.objects.filter(
                Q(
                    sale_no__icontains=query, date__icontains=date,   payment_status__icontains=payment_status) | Q(
                    customer__name__icontains=query, date__icontains=date,   payment_status__icontains=payment_status)).order_by('-updated_at')
            return queryset

    def get(self, request):
        if is_allowed_to_read_sale(request.user):
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


class SaleProducts(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SaleProductSerializers
    pagination_class = Pagination

    def get_queryset(self):
        query = self.request.GET['query']
        date = self.request.GET['date']
        queryset = SaleProduct.objects.filter(
            name__icontains=query, date__icontains=date).order_by('-updated_at')
        return queryset

    def get(self, request):
        if is_allowed_to_read_sale(request.user):
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


class SingleSale(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if is_allowed_to_read_sale(request.user):
            data = request.data
            new_Sale = Sale()
            Sale_serializer = SaleSerializers(new_Sale, data=data)
            if 'customer_name' in data and data['customer_name'] != '':
                customer = Customer.objects.get_or_create(
                    name=data['customer_name'])[0]
                new_Sale.customer = customer
            if Sale_serializer.is_valid():
                Sale_serializer.save()
                if data['products']:
                    for sale_product in data['products']:
                        sale_product_model = SaleProduct(sale=new_Sale)
                        sale_product_serializer = SaleProductSerializers(
                            sale_product_model, data=sale_product)
                        if sale_product_serializer.is_valid():
                            sale_product_serializer.save()
                        else:
                            new_Sale.delete()
                            return Response(sale_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                new_Sale.sale_no = '#'+str(new_Sale.id).zfill(4)
                new_Sale.save()
                return Response(Sale_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(Sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You are not allowed!", status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        if is_allowed_to_read_sale(request.user):
            data = request.data
            old_Sale = get_object_or_404(
                Sale, id=data['id'])
            Sale_serializer = SaleSerializers(old_Sale, data=data)
            if 'customer_name' in data and data['customer_name'] != '':
                customer = Customer.objects.get_or_create(
                    name=data['customer_name'])[0]
                old_Sale.customer = customer
            if Sale_serializer.is_valid():
                Sale_serializer.save()
                if data['products']:
                    for sale_product in data['products']:
                        diff_quantity = 0
                        if 'id' in sale_product:
                            sale_product_model = get_object_or_404(
                                SaleProduct, id=sale_product['id'])
                        else:
                            sale_product_model = SaleProduct.objects.create(
                                name=sale_product['name'], sale=old_Sale
                            )
                        sale_product_serializer = SaleProductSerializers(
                            sale_product_model, data=sale_product)
                        if sale_product_serializer.is_valid():
                            sale_product_serializer.save()
                        else:
                            old_Sale.delete()
                            return Response(sale_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(Sale_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(Sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You are not allowed!", status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, **kwargs):
        if is_allowed_to_read_sale(request.user):
            id = request.GET['sid']
            sale = get_object_or_404(
                Sale, id=id)
            sale_serializer = SaleSerializers(sale, many=False)
            return Response(sale_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('You are not allowed!', status=status.HTTP_401_UNAUTHORIZED)


class SingleSaleProduct(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        if is_allowed_to_delete_sale(request.user):
            id = request.GET['spid']
            sale_product = get_object_or_404(
                SaleProduct, id=id)
            sale_product.delete()
            return Response('Success', status=status.HTTP_200_OK)
        else:
            return Response('You are not allowed!', status=status.HTTP_401_UNAUTHORIZED)


class SingleOrderPayment(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if is_allowed_to_update_sale(request.user):
            data = request.data['data']
            payment_status = data['payment_status']
            sale = Sale.objects.get(id=data['sale_id'])
            sale.due_amount = int(sale.total) - int(data['amount'])
            sale.payment_status = payment_status
            sale.save()
            salePayment = SalePayment(sale=sale)
            payment_serializer = SalePaymentSerializers(
                salePayment, data=data)
            if payment_serializer.is_valid():
                payment_serializer.save()
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You are not allowed!", status=status.HTTP_401_UNAUTHORIZED)


class SaleReport(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if is_allowed_to_read_sale(request.user):
            today_date = request.GET['today']
            from_date = request.GET['from']
            to_date = request.GET['to']

            today_sale_number = list(Sale.objects.filter(date__icontains=today_date).annotate(dates=TruncDate(
                'date')).values('dates').annotate(count=Count('id')).values('dates', 'count').order_by('dates'))
            today_sale_prices = list(SaleProduct.objects.filter(created_at__icontains=today_date).annotate(dates=TruncDate(
                'created_at')).values('dates').annotate(price=Sum('subtotal')).values('dates', 'price').order_by('dates'))
            today_received_amounts = list(SalePayment.objects.filter(created_at__icontains=today_date).annotate(dates=TruncDate(
                'created_at')).values('dates').annotate(price=Sum('amount')).values('dates', 'price').order_by('dates'))

            sale_number = list(Sale.objects.filter(date__range=([from_date, to_date])).annotate(dates=TruncDate(
                'date')).values('dates').annotate(count=Count('id')).values('dates', 'count').order_by('dates'))
            sale_prices = list(SaleProduct.objects.filter(created_at__range=([from_date, to_date])).annotate(dates=TruncDate(
                'created_at')).values('dates').annotate(price=Sum('subtotal')).values('dates', 'price').order_by('dates'))
            received_amounts = list(SalePayment.objects.filter(created_at__range=([from_date, to_date])).annotate(dates=TruncDate(
                'created_at')).values('dates').annotate(price=Sum('amount')).values('dates', 'price').order_by('dates'))

            data = {
                'sale_numbers': {
                    'label': [],
                    'data': [],
                },
                'sale_prices': {
                    'label': [],
                    'data': [],
                },
                'received_amount': {
                    'label': [],
                    'data': [],
                },
                'today_data': {
                    'sale_prices': '',
                    'received_amounts': '',
                    'sale_numbers': ''
                }
            }
            try:
                data['today_data']['sale_prices'] = today_sale_prices[0]['price']
            except:
                pass
            try:
                data['today_data']['received_amounts'] = today_received_amounts[0]['price']
            except:
                pass
            try:
                data['today_data']['sale_numbers'] = today_sale_number[0]['count']
            except:
                pass

            for received_amount in received_amounts:
                data['received_amount']['data'].append(
                    received_amount['price'])
                data['received_amount']['label'].append(
                    received_amount['dates'])

            for prices in sale_prices:
                data['sale_prices']['label'].append(prices['dates'])
                data['sale_prices']['data'].append(prices['price'])

            for prices in sale_number:
                data['sale_numbers']['label'].append(prices['dates'])
                data['sale_numbers']['data'].append(prices['count'])

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response('You are not allowed!', status=status.HTTP_401_UNAUTHORIZED)
