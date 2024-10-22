from django.db import models
#from bookflix.gestion_pago.models import Tarjeta
import random
from gestion_pago.models import Tarjeta

# from ..\gestion_pago.models import Tarjeta
from gestion_libro.models import Libro,Capitulo
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator 


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    nickname = models.CharField(blank=False, max_length=50, null=True,)
    soyPrincipal = models.BooleanField(default=False)
    foto = models.ImageField(upload_to='static/foto_perfil',null=True, blank=True,default='static/foto_perfil/default.jpg')

    def __str__(self):
        return '%s : %s' % (self.nickname, self.user)


# class Usuario(models.Model):
    # nombre = models.CharField(max_length=50,)
    # apellido = models.CharField(max_length=50)
    # correo_electronico=models.EmailField()
    # contrasenia=models.CharField(max_length=50)
    # profile=models.ForeignKey(Profile, on_delete=models.SET_NULL,null=True,blank=True)
    # #Los libros_favoritos se obtienen con un query
    # tarjeta=models.ForeignKey(Tarjeta, on_delete=models.SET_NULL,null=True,blank=True)
    # #El historial se obtienen con un query
    # def __str__(self):
        # return '%s %s' % (self.nombre, self.apellido)

# class Perfil(models.Model):
    # nickname=models.CharField(max_length=50)
    # usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Historial(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    pagina = models.PositiveIntegerField()
    perfil = models.ForeignKey(Profile, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=True)

    def __str__(self):
        return 'de %s' % (self.perfil)

class Leidos(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    perfil = models.ForeignKey(Profile, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=True)

    def __str__(self):
        return 'de %s' % (self.libro)

class CapitulosLeidos(models.Model):
    perfil = models.ForeignKey(Profile, on_delete=models.CASCADE)
    numero_capitulo_leido = models.IntegerField(default=0,validators=[MinValueValidator(int('0'))])
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return 'de %s' % (self.perfil)

class Favorito(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    perfil = models.ForeignKey(Profile, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=True)

    def __str__(self):
        return '%s de %s' % (self.libro, self.perfil)


class Comentario(models.Model):
    perfil = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    texto = models.TextField()
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE,null=True)
    fecha = models.DateField(auto_now=True)

    def __str__(self):
        return '%s de %s' % (self.libro, self.perfil)


class Puntaje(models.Model):
    perfil = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=True)
    like = models.BooleanField(default=False,null=True, blank=True)
