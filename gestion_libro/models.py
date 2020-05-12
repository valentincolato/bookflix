from django.db import models


#from gestion_usuario.models import Usuario
# Create your models here.





class Autor(models.Model):
	nombre=models.CharField(max_length=50,default='')
	def __str__(self):		
		return '%s' % (self.nombre)

class Genero(models.Model):
	nombre=models.CharField(max_length=50,default='')
	def __str__(self):		
		return '%s' % (self.nombre)

class Editorial(models.Model):
	nombre=models.CharField(max_length=50,default='')
	def __str__(self):		
		return '%s' % (self.nombre)

class Libro(models.Model):
	nombre=models.CharField(max_length=50,default='')
	ISBN = models.CharField(max_length=50)
	autor=models.ForeignKey(Autor, on_delete=models.SET_NULL,null=True,blank=True)
	cant_capitulos = models.PositiveIntegerField()
	cant_paginas = models.PositiveIntegerField()
	genero=models.ManyToManyField(Genero)
	editorial=models.ForeignKey(Editorial, on_delete=models.SET_NULL,null=True,blank=True)
	def __str__(self):		
		return '%s : %s' % (self.nombre, self.autor)

'''
	def __str__(self):
		return '%s %s %s %s %s %s %s' % (self.ISBN, self.cant_capitulos, self.cant_capitulos, self.cant_paginas)
		
	  
'''
   