from django.db import models


#from gestion_usuario.models import Usuario
# Create your models here.





class Autor(models.Model):
    nombre=models.CharField(max_length=50)

class Genero(models.Model):
    nombre=models.CharField(max_length=50)

class Editorial(models.Model):
    nombre=models.CharField(max_length=50)

class Libro(models.Model):
    ISBN = models.CharField(max_length=50)
    autor=models.ForeignKey(Autor, on_delete=models.SET_NULL,null=True,blank=True)
    cant_capitulos = models.IntegerField()
    cant_paginas = models.IntegerField()
    genero=models.ForeignKey(Genero, on_delete=models.SET_NULL,null=True,blank=True)
    editorial=models.ForeignKey(Editorial, on_delete=models.SET_NULL,null=True,blank=True)

'''
    def __str__(self):
        return '%s %s %s %s %s %s %s' % (self.ISBN, self.cant_capitulos, self.cant_capitulos, self.cant_paginas)
        
      
'''
   