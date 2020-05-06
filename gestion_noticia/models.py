from django.db import models

# Create your models here.



class Noticia(models.Model):
    titulo = models.CharField(max_length=50)
    cuerpo = models.CharField(max_length=50)
    #foto= models.CharField(max_length=50)
