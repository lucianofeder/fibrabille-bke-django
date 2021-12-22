from django.db import models
from django.db.models.deletion import CASCADE

from ..services.user_private import Validator

class UserPrivate(models.Model):
    user = models.OneToOneField('user.User', on_delete=CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birthdate = models.DateField()
    cpf = models.CharField(max_length=14, validators=[Validator.cpf])
    mother_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
