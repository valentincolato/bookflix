from django.shortcuts import render, redirect

from .models import Libro
# Create your views here.

from gestion_usuario.views import profile_session
from gestion_usuario.models import Favorito

#proteger
def libro_especifico(request,libroId):
	l=Libro.objects.get(id=libroId)
	fav=buscar_fav(request, libroId)
	contexto={"libro":l,"favorito": fav}
	return render(request, "libroDetalle.html",contexto)

def buscar_fav(request, libroId):
	try:
		fav=(Favorito.objects.get(libro_id=libroId,perfil_id=profile_session(request)))
	except:
		fav=None
	return fav

#proteger
def libro_fav(request,libroId):
	fav=buscar_fav(request, libroId)
	if fav!=None:
		fav.delete()
	else:
		l=Libro.objects.get(id=libroId)
		per=profile_session(request)
		fav= Favorito(libro=l, perfil=per)
		fav.save()
	return redirect('/libro/'+str(libroId))
