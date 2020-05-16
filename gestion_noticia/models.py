from django.db import models

# Create your models here.



class Noticia(models.Model):
	titulo = models.CharField(max_length=50)
	cuerpo = models.TextField(blank=True)
    #foto= models.CharField(max_length=50)
	def __str__(self):
		return '%s' % (self.titulo)
