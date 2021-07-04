from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Role(TrackableDateModel):
    name = models.TextField(max_length=2000, null=True)


class RolePermission(TrackableDateModel):
    role = models.ForeignKey(Role, related_name='permissions',
                             null=True, blank=True, on_delete=models.CASCADE)
    name = models.TextField(max_length=2000, null=True)
    create = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)


class UserPermission(TrackableDateModel):
    user = models.ForeignKey(User, related_name='permissions',
                             null=True, blank=True, on_delete=models.CASCADE)
    name = models.TextField(max_length=2000, null=True)
    create = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    edit_create = models.BooleanField(default=False)
    edit_read = models.BooleanField(default=False)
    edit_update = models.BooleanField(default=False)
    edit_delete = models.BooleanField(default=False)
