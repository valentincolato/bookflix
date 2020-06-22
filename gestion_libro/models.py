from django.db import models
from django.core.validators import FileExtensionValidator

#from gestion_usuario.models import Usuario
# Create your models here.





class Autor(models.Model):
	nombre=models.CharField(max_length=50,default='',unique=True)
	def __str__(self):
		return '%s' % (self.nombre)

class Genero(models.Model):
	nombre=models.CharField(max_length=50,default='',unique=True)
	def __str__(self):
		return '%s' % (self.nombre)

class Editorial(models.Model):
	nombre=models.CharField(max_length=50,default='',unique=True)
	def __str__(self):
		return '%s' % (self.nombre)

class Libro(models.Model):
	nombre=models.CharField(max_length=50,default='')
	ISBN = models.CharField(max_length=50,unique=True)
	autor=models.ForeignKey(Autor, on_delete=models.SET_NULL,null=True,blank=True)
	cant_paginas = models.PositiveIntegerField()
	genero=models.ManyToManyField(Genero)
	editorial=models.ForeignKey(Editorial, on_delete=models.SET_NULL,null=True,blank=True)
	fecha_vencimiento = models.DateField(null=True,blank=True)
	pdf=models.FileField(upload_to='static/pdf',blank=True,null=True,validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
	nuevo_capitulo=models.FileField(upload_to='static/pdf/capitulos/',blank=True,null=True,validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
	capitulos = models.TextField(blank=True,help_text="Por favor separar cada pagina por una ',' ej: 10,30,35,102",)

	foto=models.ImageField(upload_to='static/foto_libro',blank=True, null=True)
	ocultar= models.BooleanField(default=False)
	def __str__(self):
		return '%s : %s' % (self.nombre, self.autor)

'''
	def __str__(self):
		return '%s %s %s %s %s %s %s' % (self.ISBN, self.cant_capitulos, self.cant_capitulos, self.cant_paginas)

'''
