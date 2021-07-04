from rest_framework import serializers
from .models import Sale, SaleProduct, SalePayment
from customer.serializers import CustomerSerializers


class SaleProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = SaleProduct
        fields = ['id', 'sale', 'primary_price_yuan', 'date', 'margin', 'profit', 'quantity', 'number_of_fullfilled', 'primary_price', 'sale_price',
                  'subtotal',  'name', 'link', 'image', 'created_at']


class SalePaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model = SalePayment
        fields = "__all__"


class SaleSerializers(serializers.ModelSerializer):
    products = SaleProductSerializers(many=True, read_only=True)
    customer = CustomerSerializers(many=False, read_only=True)
    payments = SalePaymentSerializers(many=True, read_only=True)
    customer_name = serializers.CharField(
        source='customer.name', read_only=True)

    class Meta:
        model = Sale
        fields = ['id',
                  'date',
                  'is_fullfilled',
                  'paid_amount',
                  'note',
                  'customer',
                  "customer_name",
                  'products',
                  'sale_no',
                  "subtotal",
                  "total",
                  "payments",
                  'payment_status',
                  'status',
                  "discount",
                  "due_amount",
                  "discount_reason",
                  "discount_type",
                  "get_voucher",
                  'paid_amount',
                  'created_at',
                  'updated_at']


class SaleListSerializers(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source='customer.name', read_only=True)

    class Meta:
        model = Sale
        fields = ['id',
                  'date',
                  'is_fullfilled',
                  "customer_name",
                  'sale_no',
                  "total",
                  'payment_status',
                  "get_voucher",
                  'paid_amount',
                  'updated_at']


class SaleProductExportSerializers(serializers.ModelSerializer):

    class Meta:
        model = SaleProduct
        fields = ['quantity', 'date', 'is_custom_product', 'number_of_fullfilled',
                  'price_per_item', 'subtotal',  'name', 'created_at']


class SalePaymentExportSerializers(serializers.ModelSerializer):
    class Meta:
        model = SalePayment
        fields = ['date', 'amount']


class SaleExportSerializers(serializers.ModelSerializer):
    products = SaleProductExportSerializers(many=True, read_only=True)
    payments = SalePaymentExportSerializers(many=True, read_only=True)
    customer_name = serializers.CharField(
        source='customer.name', read_only=True)

    class Meta:
        model = Sale
        fields = [
            'date',
            'is_fullfilled',
            'paid_amount',
            'note',
            "customer_name",
            'products',
            "subtotal",
            "total",
            "payments",
            'payment_status',
            'status',
            "discount",
            "due_amount",
            "discount_reason",
            "discount_type",
            "get_voucher",
            'paid_amount',
            'created_at',
            'updated_at']
