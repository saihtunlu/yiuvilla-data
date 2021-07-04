from django.contrib import admin
from .models import Imports, ImportProduct
# Register your models here.
model = [Imports, ImportProduct]
admin.site.register(model)
