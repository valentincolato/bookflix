from django.db import models
#from bookflix.gestion_pago.models import Tarjeta

from gestion_pago.models import Tarjeta

#from ..\gestion_pago.models import Tarjeta
from gestion_libro.models import Libro
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    fecha_nacimiento= models.DateField(null=True, blank =True)
    foto_perfil = models.ImageField(null=True, blank=True)


class Usuario(models.Model):
    nombre = models.CharField(max_length=50,)
    apellido = models.CharField(max_length=50)
    correo_electronico=models.EmailField()
    contrasenia=models.CharField(max_length=50)
    profile=models.ForeignKey(Profile, on_delete=models.SET_NULL,null=True,blank=True)
    #Los libros_favoritos se obtienen con un query
    tarjeta=models.ForeignKey(Tarjeta, on_delete=models.SET_NULL,null=True,blank=True)
    #El historial se obtienen con un query
    def __str__(self):        
         return '%s %s' % (self.nombre, self.apellido)

class Perfil(models.Model):
    nickname=models.CharField(max_length=50)
    usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)    

class Historial(models.Model):
    libro=models.ForeignKey(Libro, on_delete=models.CASCADE)
    pagina=models.IntegerField()
    perfil=models.ForeignKey(Perfil, on_delete=models.CASCADE)

class Favorito(models.Model):
    libro=models.ForeignKey(Libro, on_delete=models.CASCADE)
    pagina=models.IntegerField()
    perfil=models.ForeignKey(Perfil, on_delete=models.CASCADE)


class Comentario(models.Model):
    usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto= models.CharField(max_length=50)
    libro=models.ForeignKey(Libro, on_delete=models.CASCADE)



