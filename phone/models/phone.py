from django.db import models
from django.db.models.deletion import CASCADE

from ..services.phone import PhoneServices, Validator

class Phone(models.Model):
    phone = models.CharField(max_length=10)
    ddd = models.CharField(max_length=2)
    user = models.ForeignKey("user.User", on_delete=CASCADE, related_name="phone_list", null=True)

    def save(self, *args, **kwargs):
        Validator.phone(self.phone)
        self.ddd, self.phone = PhoneServices.split_phone(self.phone)
        super(Phone, self).save(*args, **kwargs)