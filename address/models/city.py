from django.db import models
from django.db.models.deletion import CASCADE


class City(models.Model):
    city = models.CharField(max_length=50)
    state = models.ForeignKey("address.State", on_delete=CASCADE)
    ibge = models.CharField(max_length=50)
    