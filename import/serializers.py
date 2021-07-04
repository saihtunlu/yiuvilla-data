from rest_framework import serializers
from .models import Imports, ImportProduct


class ImportProductSerializers(serializers.ModelSerializer):

    class Meta:
        model = ImportProduct
        fields = [
            'id', 'imports',  'primary_price_yuan', 'date', 'margin', 'profit', 'quantity', 'number_of_fullfilled', 'primary_price', 'sale_price',
                  'subtotal',  'name', 'link', 'image', 'created_at']


class ImportsSerializers(serializers.ModelSerializer):
    products = ImportProductSerializers(many=True, read_only=True)

    class Meta:
        model = Imports
        fields = ['id',
                  'date',
                  'products',
                  'note',
                  'total',
                  'created_at',
                  'updated_at', ]
