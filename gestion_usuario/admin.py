from django.contrib import admin
from django.contrib.auth.models import User
from django.conf.urls import url
from django import forms
from gestion_usuario.models import Favorito, Comentario, Historial, Profile, Puntaje,Leidos, CapitulosLeidos
from django.contrib.admin import SimpleListFilter, DateFieldListFilter,FieldListFilter


# Register your models here.
# admin.site.register(Usuario)
#admin.site.register(Perfil)
admin.site.register(Historial)
admin.site.register(Comentario)
admin.site.register(Profile)
admin.site.register(Puntaje)
admin.site.register(Favorito)
#admin.site.register(Leidos)
#admin.site.register(CapitulosLeidos)

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'date_joined', 'is_staff']
    actions = ['Informe_entre_dos_fechas']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
