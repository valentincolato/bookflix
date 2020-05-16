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
from gestion_usuario.views import home,welcome,register,login,logout,edit_profile,profile,index
from gestion_noticia.views import news,news_especifica
from gestion_libro.views import libro_especifico
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    # path('',welcome),
    path('register',register),
    path('login',login),
    path('logout',logout),
    path('profile/edit_profile/', edit_profile),
    path('profile/', profile),
    path('news/', news),
	path('news/<newsId>', news_especifica),
    path('libro/<libroId>', libro_especifico),
    path('index', index),

]
urlpatterns+= staticfiles_urlpatterns()