from django.db import models
from django.db.models.deletion import CASCADE

from ..services.address import AdressServices

class Address(models.Model):
    is_commercial = models.BooleanField(default=False)
    zip_code = models.CharField(max_length=9)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=50)
    complement = models.CharField(max_length=1028)
    district = models.CharField(max_length=100)
    city = models.ForeignKey("address.City", on_delete=CASCADE)

    def save(self, *args, **kwargs):
        self = AdressServices.get_data_from_zip_code(self)
        if len(self.zip_code) == 8:
            self.zip_code = f"{self.zip_code[:5]}-{self.zip_code[5:]}"

        return super(Address, self).save(*args, **kwargs)


