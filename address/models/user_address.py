from django.db import models
from django.db.models.deletion import CASCADE


class UserAddress(models.Model):
    address_charge = models.ForeignKey('address.Address', on_delete=CASCADE, related_name="charging_for")
    address_instalation = models.ForeignKey('address.Address', on_delete=CASCADE, related_name="instalation_for")
    contact = models.CharField(max_length=256)
    wireless_login = models.CharField(max_length=100)
    wireless_password = models.CharField(max_length=100)
    onu_login = models.CharField(max_length=100)
    onu_password = models.CharField(max_length=100)
    user = models.ForeignKey("user.User", on_delete=CASCADE, related_name="address_list")


    def save(self, *args, **kwargs):
        if not hasattr(self, "address_charge"):
            self.address_charge = self.address_instalation
        return super(UserAddress, self).save(*args, **kwargs)