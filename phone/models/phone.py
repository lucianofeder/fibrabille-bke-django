from django.db import models

from ..services.phone import PhoneServices, Validator

class Phone(models.Model):
    phone = models.CharField(max_length=10)
    ddd = models.CharField(max_length=2)

    def save(self, *args, **kwargs):
        Validator.phone(self.phone)
        self.ddd, self.phone = PhoneServices.split_phone(self.phone)
        super(Phone, self).save(*args, **kwargs)