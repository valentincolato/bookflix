from django.db import models

# Create your models here.
class Tarjeta(models.Model):
    numero = models.IntegerField()
    cvc = models.IntegerField()