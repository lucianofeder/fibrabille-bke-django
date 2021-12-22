from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from ..services.user import UserManager

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_sales_rep = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    extra_info = models.CharField(max_length=256)
    blocked = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = UserManager()