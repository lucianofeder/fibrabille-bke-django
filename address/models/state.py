from django.db import models


class State(models.Model):
    state = models.CharField(max_length=50, unique=True)
    uf = models.CharField(max_length=2, unique=True)
    uf_code = models.CharField(max_length=2, unique=True)
