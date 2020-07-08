"""bookflix URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,re_path
from gestion_usuario.views import home,welcome,register,login,logout,edit_profile,profile,index,change_profile_view,change_session_profile,register_profile,desactivar_perfil,historial,informe_usuario,borrar_comentario,terminar_lectura
from gestion_noticia.views import news,news_especifica,trailer,trailer_especifico
from gestion_libro.views import home_logueado,libro_especifico,libro_fav,SearchResultsView,libro_no_disponible,informe_libro,add_capitulo,edit_capitulo
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/informe_usuario', informe_usuario),
    path('admin/informe_libro', informe_libro),
    path('admin/gestion_libro/agregar_capitulo/<id_libro>', add_capitulo),
    path('admin/gestion_libro/editar_capitulo/<id_capitulo>', edit_capitulo),
    path('', home),
    # path('',welcome),
    path('register',register),
    path('login',login),
    path('logout',logout),
    path('profile/', profile),
    path('profile/edit_profile/', edit_profile),
    path('profile/desactivar_perfil/<id>', desactivar_perfil),
    path('libro/borrar_comentario/<id>', borrar_comentario),
    path('libro/terminar_lectura/<libro_id>', terminar_lectura),
    path('change_profile/', change_profile_view),
    path('change_profile/<id>', change_session_profile),
    path('register_profile', register_profile),
    path('historial', historial),
    path('news/', news),
	path('news/<newsId>', news_especifica),
    path('libro/<libroId>', libro_especifico),
    path('home/', home_logueado),
	path('fav/<libroId>', libro_fav),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('index', index),
	path('libronodisponible', libro_no_disponible),
    path('trailer', trailer),
    path('trailer/<trailerId>', trailer_especifico),
    

]
urlpatterns+= staticfiles_urlpatterns()

# Añadir
admin.site.site_header = 'Administracion Bookflix'
