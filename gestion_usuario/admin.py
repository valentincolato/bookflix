from django.contrib import admin

from gestion_usuario.models import Usuario,Perfil,Favorito,Comentario,Historial,Profile



# Register your models here.
admin.site.register(Usuario)
admin.site.register(Perfil)
admin.site.register(Historial)
admin.site.register(Comentario)
admin.site.register(Profile)
admin.site.register(Favorito)