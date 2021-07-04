from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(TrackableDateModel):
    name = models.TextField(max_length=2000, null=True)
    phone = models.TextField(max_length=2000, blank=True, null=True)

    def __unicode__(self):
        return self.name
