from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Q


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.TextField(
        max_length=2000,  default='/media/default.png', null=True)
    role = models.TextField(
        max_length=2000,  default='customer', null=True)
    phone = models.TextField(
        max_length=2000, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'
