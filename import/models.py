from django.db import models


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Imports(TrackableDateModel):
    note = models.TextField(max_length=2000, null=True, default="")
    date = models.TextField(max_length=2000, null=True, blank=True)
    total = models.TextField(null=True, default=0)


class ImportProduct(TrackableDateModel):
    imports = models.ForeignKey(Imports, related_name='products',
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
