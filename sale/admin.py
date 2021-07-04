from django.contrib import admin
from .models import Sale, SaleProduct, SalePayment
# Register your models here.
models = [SaleProduct, Sale, SalePayment]
admin.site.register(models)
