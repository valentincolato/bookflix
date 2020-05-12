from django.contrib import admin

from gestion_usuario.models import Favorito,Comentario,Historial,Profile,Puntaje



# Register your models here.
# admin.site.register(Usuario)
# admin.site.register(Perfil)
admin.site.register(Historial)
admin.site.register(Comentario)
admin.site.register(Profile)
admin.site.register(Puntaje)
admin.site.register(Favorito)