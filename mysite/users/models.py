from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    ROLE_CHOICES = [
        ('менеджер', 'manager'),
        ('водитель', 'driver'),
    ]
    role = models.CharField(max_length=8, choices=ROLE_CHOICES, default='user', verbose_name=_("role"))
