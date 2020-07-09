from django.db import models
from django.core.validators import FileExtensionValidator,MinValueValidator 
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
	ocultar= models.BooleanField(default=False)
	foto=models.ImageField(upload_to='static/foto_libro',blank=True, null=True)
	pdf=models.FileField(upload_to='static/pdf',editable = False,blank=True,null=True,validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
	es_capitulado = models.BooleanField(default=False)
	numero_de_capitulos= models.IntegerField(default=0,editable = False, validators=[MinValueValidator(int('1'))])
	def __str__(self):
		return '%s : %s' % (self.nombre, self.autor)

'''
	def __str__(self):
		return '%s %s %s %s %s %s %s' % (self.ISBN, self.cant_capitulos, self.cant_capitulos, self.cant_paginas)

'''
class Capitulo(models.Model):
	numero_de_capitulo= models.IntegerField(validators=[MinValueValidator(int('0'))])
	pdf = models.FileField(upload_to='static/pdf/capitulos/',blank=True,null=True,validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
	libro = models.ForeignKey(Libro, on_delete=models.CASCADE,null=True,blank=True,editable = False)
	def __str__(self):
		return '%s' % (self.numero_de_capitulo)
