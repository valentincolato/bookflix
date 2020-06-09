from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Tarjeta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    numero = models.IntegerField()
    cvc = models.IntegerField()
    tipo_suscripcion= models.CharField(max_length=50,default='regular')