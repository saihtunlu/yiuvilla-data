from customer.models import Customer
from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Sale(TrackableDateModel):
    sale_no = models.TextField(max_length=2000, null=True, unique=True)
    customer = models.ForeignKey(Customer, related_name='sales',
                                 null=True, blank=True, on_delete=models.CASCADE)
    subtotal = models.TextField(max_length=2000, null=True, default="0")
    total = models.IntegerField(null=True, default=0)
    discount = models.TextField(max_length=2000, null=True, default="0")
    paid_amount = models.TextField(max_length=2000, null=True, default="0")
    discount_reason = models.TextField(max_length=2000, null=True, blank=True)
    discount_type = models.TextField(max_length=2000, null=False, default='Ks')
    due_amount = models.TextField(max_length=2000, default='0', blank=True)
    payment_status = models.TextField(
        max_length=2000, default='Unpaid', blank=True)
    status = models.TextField(max_length=2000, null=True, default='Processing')
    note = models.TextField(max_length=2000, null=True, default="")
    date = models.DateTimeField(null=True, blank=True)
    is_fullfilled = models.BooleanField(default=False)
    get_voucher = models.BooleanField(default=False)


class SaleProduct(TrackableDateModel):
    sale = models.ForeignKey(Sale, related_name='products',
                             null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.TextField(max_length=2000, null=True, default="0")
    number_of_fullfilled = models.TextField(
        max_length=2000, null=True, default="0")
    primary_price = models.TextField(max_length=2000, null=True, default="0")
    primary_price_yuan = models.TextField(
        max_length=2000, null=True, default="0")
    sale_price = models.TextField(max_length=2000, null=True, default="0")
    subtotal = models.TextField(max_length=2000, null=True, default="0")
    margin = models.TextField(max_length=2000, null=True, default="0")
    profit = models.TextField(max_length=2000, null=True, default="0")
    name = models.TextField(max_length=2000, null=True, blank=True)
    image = models.TextField(max_length=2000, null=True, blank=True)
    link = models.TextField(max_length=2000, null=True, blank=True)
    date = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class SalePayment(TrackableDateModel):
    sale = models.ForeignKey(Sale, related_name='payments',
                             null=True, blank=True, on_delete=models.CASCADE)
    amount = models.TextField(max_length=2000, default='0', blank=True)
    date = models.TextField(max_length=2000, default='0', blank=True)
