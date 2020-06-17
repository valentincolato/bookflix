from django.db import models
from gestion_libro.models import Libro
from django.core.validators import FileExtensionValidator

# Create your models here.



class Noticia(models.Model):
	titulo = models.CharField(max_length=50)
	cuerpo = models.TextField(blank=True)
	fecha_de_creacion = models.DateField()
	def __str__(self):
		return '%s' % (self.titulo)


class Trailer(models.Model):
	titulo = models.CharField(max_length=50)
	cuerpo = models.TextField(blank=True)
	libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
	video=models.FileField(upload_to='static/video_trailer',blank=True,null=True,validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
	fecha_de_creacion = models.DateField()
	def __str__(self):
		return '%s' % (self.titulo)
