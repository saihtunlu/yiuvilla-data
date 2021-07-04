from django.db import models

# Create your models here.
from django.db import models


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class File(TrackableDateModel):
    image = models.ImageField(
        upload_to='images/%Y/%m/%d/', default='/default.png', blank=True, null=True)
    file = models.FileField(
        upload_to='files/%Y/%m/%d/',  blank=True, null=True)

    def __str__(self):
        return self.image
